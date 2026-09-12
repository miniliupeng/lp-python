# 大厂高频面试题精讲 (04-02-asyncio-event-loop-core)

---

### Q1: 请详述 asyncio 事件循环的底层运行机制。协程（Coroutine）、任务（Task）与 Future 有何本质区别？

#### 🎯 面试官考点
- 操作系统 I/O 多路复用（epoll/kqueue）、三者在状态机与调度上的定位差异。

#### 💡 满分回答模板
1. **事件循环底层（Reactor 模式）**：
   - 底层由标准库 `selectors` 驱动，在 Linux 上使用 **`epoll`**，在 macOS 上使用 **`kqueue`**；
   - 事件循环在单线程中循环运行：向内核注册 Socket 描述符的读写事件，线程进入休眠；当有网络数据到达时内核唤醒事件循环，分发执行回调；
2. **三者的本质区别**：
   - **`Coroutine`（协程，待执行蓝图）**：由 `async def` 声明的函数调用产物。它是**惰性的**，如果不主动 `await` 它或将其包装进 Task，它**绝对不会自动执行任何代码**；
   - **`Future`（期物，低级结果容器）**：代表一个**可能尚未完成的异步操作最终结果载体**。它维护了 `PENDING`, `CANCELLED`, `FINISHED` 三大状态与回调函数列表；
   - **`Task`（任务，调度管理者）**：**是 `Future` 的直接子类**。当调用 `asyncio.create_task(coro)` 时，Task 负责将协程注册挂载到当前事件循环中，并在协程每次 `yield/await` 时自驱动调用其 `send()`，是协程并发执行的载体。

---

### Q2: 为什么在 async 函数内部绝对严禁调用同步阻塞代码（如 time.sleep 或 requests.get）？如何正确治理？

#### 🎯 面试官考点
- 协作式调度的脆弱性、事件循环饥饿与多线程线程池卸载。

#### 💡 满分回答模板
1. **灾难根源：协作式调度（Cooperative Multitasking）的单线程本质**：
   - `asyncio` 并不是抢占式调度的（操作系统不会主动强行切换协程），协程的让步**全凭自身自觉写了 `await` 出让 CPU**；
   - 一旦在协程里执行了同步阻塞调用（如 `time.sleep(10)`），当前操作系统的唯一执行线程将被物理挂起 10 秒；
   - **后果**：整个进程的事件循环彻底停摆，**没有任何其他就绪任务、网络回调能被分发执行**，线上数千个正在通信的用户接口将同时被超时熔断！
2. **标准生产治理方案**：
   - **网络替换为纯异步库**：用 `httpx.AsyncClient` 替代 `requests`，用 `asyncio.sleep` 替代 `time.sleep`；
   - **必须使用同步库时（如老旧 SDK/本地磁盘 I/O）**：
     必须调用 **`asyncio.to_thread(func, *args)`**（Python 3.9+）将其包装卸载到底层后台线程池执行，事件循环仅需 `await` 对应线程的完成信号，绝不阻塞主循环。

---

### Q3: asyncio.run() 的底层生命周期包含哪些步骤？为什么在一个已经运行的事件循环中不能再次调用 asyncio.run()？

#### 🎯 面试官考点
- 事件循环生命周期管理、递归创建事件循环的冲突与嵌套运行防范。

#### 💡 满分回答模板
1. **`asyncio.run(main())` 的完整生命周期**：
   - **创建全新循环**：调用 `new_event_loop()` 并设为当前线程上下文主循环；
   - **驱动主协程运行**：调用 `loop.run_until_complete(main())` 持续分发事件直到主协程完成；
   - **取消所有残留任务**：获取所有未完成的残留 Task（`all_tasks()`），逐一发送 `cancel()` 并等待退出；
   - **关闭异步生成器与优雅析构**：调用 `shutdown_asyncgens()` 与 `shutdown_default_executor()`；
   - **彻底关闭并销毁循环**：调用 `loop.close()` 释放底层资源。
2. **为什么禁止嵌套调用**：
   - `asyncio.run()` 的设计前提是**作为整个应用程序的唯一顶层入口**；
   - 事件循环是单线程不可重入的（Non-reentrant）。如果在某个协程内部再次调用 `asyncio.run()`，会抛出 `RuntimeError: This event loop is already running`，防止多个事件循环在同一线程产生无法协调的状态污染。
