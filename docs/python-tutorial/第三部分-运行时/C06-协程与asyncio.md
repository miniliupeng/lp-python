# C06　asyncio

> 示例：`examples/part_c/c06_asyncio.py`

## 学完你能做什么

写出一个有结构的并发任务组，把阻塞函数移出事件循环，并正确对待取消。

## 一个线程里的协作式调度

`asyncio` 在一个线程里运行事件循环。协程执行到 `await` 才可能让出。在此之前，别的协程不会插进来。没有 `await` 的长循环会卡住整个循环，包括超时和取消检查。

这和线程不同。线程可以由 GIL 的切换间隔打断。协程不会。所以 asyncio 不是“更轻的线程”，它是另一套调度约定：你在等待点显式让路。

`asyncio.run(coro)` 创建循环、跑完这个协程、关闭循环。它是程序的入口。不要在已经运行的循环里再调用 `asyncio.run`。库函数应当是协程，由调用方决定在哪个循环里跑。

## `TaskGroup`

3.11 起的 `asyncio.TaskGroup` 是结构化并发。示例在组里创建两个加法任务，离开 `async with` 时两个都结束了，然后才读结果。组里有任务失败，其余任务会被取消，异常以 `ExceptionGroup` 的形式冒出来。不要再新写一堆裸的 `create_task` 然后忘掉 `await`。忘掉的任务会在后面随机报错，或者拖住退出。

`asyncio.timeout` 同样从 3.11 开始。示例用 1 秒包住一个立刻完成的 `sleep(0)`，证明这个 API 在 3.12 可用。超时到期抛 `TimeoutError`。超时也会取消里面的等待。

`sleep(0)` 只是把控制权交回循环一次，方便测试。生产代码里它不是调度策略。你应该 `await` 真正的 I/O。

## 取消

`task.cancel()` 请求在下一个等待点抛出 `CancelledError`。这个类继承 `BaseException`，不继承 `Exception`。示例先断言了继承关系，再取消一个睡 10 秒的任务。`except Exception` 接不住取消，这是故意的：清理代码不应该把取消当成普通失败吞掉。

要做清理，用 `finally` 或 `with`，清理完重新抛出 `CancelledError`。吞掉它会让 `TaskGroup` 以为任务正常结束，结构化并发就失效了。

取消是协作的。卡在没有 `await` 的纯 Python 循环里的协程，看不到取消。CPU 工作不要放进协程。

## 阻塞调用

`asyncio.to_thread` 把函数交给线程池，在线程里跑，事件循环继续。示例把返回 7 的函数这样调用。适合少量、会阻塞的现成函数。大量 CPU 计算不该丢进默认线程池，那只是把 GIL 下的计算换了个线程，循环是不卡了，核数并没有用上。CPU 计算用进程，或者在 C07 的条件下用自由线程构建。

`time.sleep` 在协程里会卡住循环。等待时间用 `await asyncio.sleep`。阻塞的文件和网络 API 不要在协程里直接调，除非那个库声明自己会释放控制权。

## 锁也是两套

`asyncio.Lock` 只保护协程之间的临界区，并且必须在持有它的同一个循环里 `await`。它不能用来和另一个操作系统线程互斥。线程之间用 `threading.Lock`。两边都碰同一份数据时，先把数据的主人定成一个：要么只在循环线程里改，要么只用队列把操作送过去。

## 机制

asyncio 在一个线程里跑多个协程。切换只发生在 `await` 把控制权交还给事件循环的时候。没有 `await` 的长循环会堵住所有协程。这和线程抢占不同。

协程函数调用后得到协程对象，不会自动执行。要把它交给事件循环：`asyncio.run` 是进程里跑一次主协程的入口。一个线程通常一个循环。

`Task` 是被调度的协程。`TaskGroup` 从 3.11 进入标准库，负责结构化并发：一组任务一起开始，有一个失败就取消同组的其它任务，退出 `async with` 时等待它们结束。异常以 `ExceptionGroup` 抛出。不要再手写“创建一堆 Task 然后忘了 await”。

取消：`task.cancel()` 在任务下一次让出时注入 `CancelledError`。它继承 `BaseException`，不继承 `Exception`。`except Exception` 抓不住它。抓了 `CancelledError` 做清理后必须重新抛出，否则任务看起来取消了却继续跑。3.8 以前它是 `Exception` 的子类，旧文章会说错。

超时用 `asyncio.timeout`（3.11）或 `wait_for`。超时的结果是取消。清理逻辑要放在 `finally` 或 `with` 里。

阻塞调用不能直接放进协程。`time.sleep` 会冻住循环，`asyncio.sleep` 才会让出。文件和老的数据库驱动如果是阻塞的，用 `asyncio.to_thread` 放到线程里。那条线程仍受 GIL 约束，但至少循环还能调度别的协程。

锁也是两套。`asyncio.Lock` 只在协程之间排队，不阻止操作系统线程。`threading.Lock` 才能管线程。在协程里拿着线程锁再 `await`，可能把线程池卡死。不要混用。

`contextvars` 会随着 Task 拷贝上下文。它不会自动进入你用 `threading.Thread` 新开的线程。跨线程要显式传。

## 会出事的写法

- 在协程里 `requests.get` 或 `time.sleep`。整个循环停住。
- `create_task` 之后不保存引用。任务可能被回收，还没跑完。
- 捕获 `ExceptionGroup` 后只处理第一个错误，其余任务的失败被丢掉。
- 取消后吞掉 `CancelledError`。调用方以为资源已经释放，协程还在写。

## 示例对照

`examples/part_c/c06_asyncio.py` 用 `TaskGroup` 跑多个协程，断言它们都完成，并证明阻塞与让出的差别是行为而不是秒表：该让出的地方用 `asyncio.sleep(0)` 或很短的 `sleep`，断言结果的顺序或集合。取消测试如果有，必须断言被取消的任务停了，而不是吞掉异常后继续返回成功。

## 加练

1. 为什么 `except Exception` 里写“记录然后返回”会破坏取消？
2. `asyncio.Lock` 能防止两个线程同时改一个列表吗？

参考答案：

1. 取消异常不是 `Exception` 的子类，所以这条语句本来抓不住。如果有人写成 `except BaseException` 然后返回，取消就被吞了。清理后要重新抛出。
2. 不能。它只协调同一个线程里的协程。两个操作系统线程要用线程锁，或者不要共享这个列表。

## 面试

### Q1. asyncio 什么时候切换任务？

**考点**：协作式，不是抢占。

**回答**：

1. 只在 `await` 让出时。事件循环再挑选就绪的任务。
2. CPU 密集循环不写 `await`，其它协程就饿死。
3. 这种循环应放到进程或 `to_thread`，不要假装它是异步的。

### Q2. `TaskGroup` 解决什么问题？

**考点**：结构化并发。

**回答**：

1. 一组任务的生命周期绑在一个作用域上。离开作用域前它们都结束。
2. 一个失败，其余被取消，异常成组抛出。
3. 这避免了“后台 Task 抛了异常没人 await”的丢失失败。3.11 之前要用第三方库或仔细管理 `gather(return_exceptions=...)`。

### Q3. 协程里能用线程池吗？

**考点**：阻塞和 GIL 的边界。

**回答**：

1. 能。`asyncio.to_thread` 或 `run_in_executor` 把阻塞函数放到线程。
2. 线程里仍不要跑纯 Python 大计算指望多核。那是进程的事。
3. 回到协程的对象要线程安全地移交。不要在线程里直接改还会被协程读取的结构，除非有锁。

## 常见错误

- 在协程里调用 `requests.get` 这类阻塞客户端，然后觉得 asyncio 很慢。循环被这一次调用占住了。用异步客户端，或 `to_thread`。
- 捕获 `Exception` 时把 `CancelledError` 一起“处理掉”。3.8 以后这样已经捕获不到了；如果有人把它改回捕获 `BaseException`，就会再次吞掉取消。
- 任务创建后不加入 `TaskGroup`，进程退出时出现“task was destroyed but it is pending”。

## 练习

1. 两个协程各 `await asyncio.sleep(0)` 后返回自己的参数。用 `TaskGroup` 收集结果。
2. 为什么取消要继承 `BaseException`？
3. 什么工作不该放进协程本体？

参考答案：

1. 结构和示例的 `coordinated` 相同，把 `add_later` 换成返回参数本身即可。
2. 这样普通的 `except Exception` 不会把取消当成业务失败吃掉，清理后的取消仍能继续传播。
3. 长时间占用 CPU、不 `await` 的循环，以及会阻塞线程的库调用。

## 小结

asyncio 在单线程里按等待点切换。`TaskGroup` 和 `timeout` 划出任务的生命周期。`CancelledError` 不是 `Exception`。阻塞函数用 `to_thread`，CPU 密集不要伪装成协程。
