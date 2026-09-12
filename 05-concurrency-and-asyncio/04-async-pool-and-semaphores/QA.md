# 大厂高频面试题精讲 (04-04-async-pool-and-semaphores)

---

### Q1: 如果需要并发请求 10,000 个第三方 API，直接使用 asyncio.gather(*tasks) 会导致什么致命后果？

#### 🎯 面试官考点
- 系统级资源极限（FD/Socket/RAM）、微服务雪崩效应与连接池防御。

#### 💡 满分回答模板
1. **操作系统文件描述符耗尽（FD Exhaustion）**：
   - 每个出站 TCP 连接都会占用一个文件描述符；操作系统对单进程最大打开文件数有默认限制（如 Linux 默认 `ulimit -n 1024`）；
   - 瞬间创建 10,000 个连接会直接抛出 **`OSError: [Errno 24] Too many open files`**，不仅当前网络全部失败，连进程读取本地日志或文件都会一并崩溃。
2. **对端服务被打垮或被反爬封禁**：
   - 瞬间高密度的流量洪峰会直接将目标下游服务的连接池或网关 CPU 打满，触发 502/504 超时甚至触发 WAF 防火墙封禁本机 IP。
3. **V8/Python 堆内存暴涨**：
   - 一次性在内存中实例化 10,000 个中间 Task 和闭包上下文对象，内存瞬间暴增，引起剧烈的垃圾回收停顿。

---

### Q2: 如何手写一个带并发限制的异步任务执行器？请阐明其核心设计思想。

#### 🎯 面试官考点
- 信号量调度原理、槽位防泄漏与异常安全。

#### 💡 满分回答模板
1. **核心思想（Semaphore 滑动窗口）**：
   - 实例化一个 `asyncio.Semaphore(limit)`；
   - 将每个异步调用用 `async with sem:` 包裹；
   - 协程在进入代码块前必须抢占信号量槽位，执行完毕后在 `finally` 中归还槽位，未获取槽位的任务被挂起在等待队列中，实现匀速推进。
2. **极简且健壮的工业级代码实现**：
   ```python
   import asyncio


   async def run_with_limit(tasks, limit: int = 10):
       sem = asyncio.Semaphore(limit)

       async def sem_task(coro):
           async with sem:
               return await coro

       return await asyncio.gather(*(sem_task(t) for t in tasks))
   ```

---

### Q3: 什么是异步流控中的“背压（Backpressure）”？在数据洪峰场景下如何利用 asyncio.Queue 阻止上游压垮下游？

#### 🎯 面试官考点
- 生产者-消费者模式、有界队列（Bounded Queue）与反应式流控原理。

#### 💡 满分回答模板
1. **背压（Backpressure）的核心定义**：
   - 当**数据的生产速率远高于下游的消费处理速率**时，下游反向向上游施加阻力，迫使上游主动放慢生产节奏，防止系统内存溢出。
2. **基于 `asyncio.Queue(maxsize=N)` 的实现原理**：
   - 如果使用无界队列（默认 `maxsize=0`），上游会疯狂向内存中塞入数百万条数据，最终导致进程 OOM；
   - **配置有界上限**：声明 `queue = asyncio.Queue(maxsize=100)`；
   - 当下游处理慢导致队列中堆积满 100 条数据时，生产者执行 **`await queue.put(item)` 将被物理挂起暂停**；
   - 只有当下游消费者处理完一条并执行 `queue.get()` 挪出空位时，事件循环才会唤醒生产者继续读取下一条数据，实现了极其优美且自动化的端到端背压流控。
