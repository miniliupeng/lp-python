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
