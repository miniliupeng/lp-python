# 专题 02：asyncio 单线程协作式事件循环、Task 调度与 Future 状态机

在现代高并发后端架构中，传统的“一连接一线程（Thread-per-connection）”模型在海量并发面前因内存暴涨与系统调度瓶颈而失效。Python 标准库内置的 **`asyncio`** 采用了与 Node.js 类似的思想：基于**单线程异步非阻塞 I/O + 事件循环（Event Loop）**，使单台服务器能够轻松支撑数以万计的并发长连接。

---

## 一、 痛点驱动：同步阻塞对单线程事件循环的致命摧毁

在异步协程开发中，最大的禁忌是**混入同步阻塞调用**：
```python
async def handle_request():
    time.sleep(5)  # ❌ 灾难: 整个进程的主事件循环被物理冻结 5 秒！
    return "ok"
```
由于事件循环运行在单线程上，一旦某个协程执行了同步休眠或阻塞式文件/网络调用，**全站所有其他用户的并发请求将全部被死锁挂起**，造成雪崩式服务超时。

---

## 二、 机制解密：Coroutine、Task 与 Future 的三位一体

```text
[ asyncio 事件循环运转拓扑 ]
  1. 协程对象 (Coroutine): async def 产生的惰性生成器包装
         │
         ▼ (通过 asyncio.create_task() 注册进事件循环)
  2. 任务对象 (Task): 继承自 Future，负责将协程步进执行驱动至下一个 await
         │
         ▼ (在底层 selectors 注册 epoll/kqueue 非阻塞监听)
  3. 期物对象 (Future): 代表一个尚未完成的底层异步 I/O 结果载体 (PENDING -> FINISHED)
```

1. **`await` 的本质**：
   - `await expr` 只能等待一个可等待对象（Awaitable: Coroutine, Task, Future）；
   - 它在底层等价于将当前协程挂起并出让 CPU 控制权，通知事件循环：“当该 I/O 完成后，再唤醒我继续向下执行”；
2. **`asyncio.create_task()` 实现真正的单线程并发**：
   - 单纯写 `await fn()` 是顺序串行执行；
   - 只有将协程通过 `asyncio.create_task()` 包装成 Task，它才会被立即推入事件循环就绪队列，实现并发交替推进。

---

## 三、 生产规范与避坑指南

- **坚决杜绝同步阻塞库**：HTTP 请求严禁使用 `requests`（必须使用 `httpx` 或 `aiohttp`）；数据库操作严禁使用同步驱动；
- **同步密集计算必须卸载（Offloading）**：不可避免的 CPU 计算必须调用 `asyncio.to_thread()` 将其卸载到底层线程池执行，坚决不阻塞主事件循环。
