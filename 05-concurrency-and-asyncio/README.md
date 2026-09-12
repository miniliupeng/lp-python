# 阶段 05: 并发编程、GIL 与现代 Asyncio

并发模型是后端服务吞吐能力的上限。本阶段从 CPython GIL 的底层约束与 Free-threaded 演进，深入到现代 Python 3.11+ 的 `asyncio.TaskGroup` 结构化并发、协程任务调度与连接池信号量治理。

---

## 💡 核心工程心智与底层机制

1. **GIL 本质与多线程/多进程选型**：
   - 全局解释器锁（GIL）确保 CPython 内部引用计数与 C 扩展的线程安全，但也导致多线程无法利用多核 CPU 执行计算密集型任务；
   - I/O 密集型使用多线程/协程，CPU 密集型使用 `multiprocessing` 多进程或外部 C 扩展；密切关注 Python 3.13+ Free-threaded（PEP 703）无 GIL 演进。
2. **事件循环（Event Loop）核心机制**：
   - 基于操作系统的多路复用 I/O（Linux epoll / macOS kqueue）；
   - 协作式非抢占调度，利用 `await` 主动让出 CPU 执行权；任何耗时 CPU 密集型任务必须使用 `run_in_executor` 剥离，避免卡死整个事件循环。
3. **TaskGroup 结构化并发（Structured Concurrency）**：
   - 彻底废弃易导致协程泄漏、孤儿任务失控的旧式 `asyncio.gather`；
   - 拥抱 Python 3.11+ `asyncio.TaskGroup` 与上下文管理器语法，确保并发任务“同生共死”，结合 `ExceptionGroup` 实现统一错误处理。
4. **异步并发限流与信号量池化**：
   - 无节制地派发并发请求会瞬间击垮下游数据库或触发第三方 API 限流封禁；
   - 掌握利用 `asyncio.Semaphore` 实施精细化并发度削峰填谷，构建生产级稳态连接池。

---

## 🗺️ 阶段专题导航

| 专题目录 | 核心原语 | 关键掌握目标 |
| :--- | :--- | :--- |
| **[01-threading-multiprocessing-gil](./01-threading-multiprocessing-gil/)** | GIL 约束与多进程/多线程选型 | 掌握 CPU 密集与 I/O 密集型并发基准对比与 Free-threaded 前沿演进 |
| **[02-asyncio-event-loop-core](./02-asyncio-event-loop-core/)** | 事件循环运行机制 | 掌握 epoll/kqueue 事件驱动循环、协作调度与阻塞操作安全脱耦 |
| **[03-structured-concurrency-taskgroup](./03-structured-concurrency-taskgroup/)** | TaskGroup 结构化并发 | 掌握生命周期绑定、异常快速失败熔断与 ExceptionGroup 捕获 |
| **[04-async-pool-and-semaphores](./04-async-pool-and-semaphores/)** | 异步信号量与并发池化 | 掌握 `asyncio.Semaphore` 限流防压垮、并发任务槽位调度与背压防护 |

---

## 🚀 统一运行验证

```bash
uv run python 05-concurrency-and-asyncio/01-threading-multiprocessing-gil/main.py
uv run python 05-concurrency-and-asyncio/02-asyncio-event-loop-core/main.py
uv run python 05-concurrency-and-asyncio/03-structured-concurrency-taskgroup/main.py
uv run python 05-concurrency-and-asyncio/04-async-pool-and-semaphores/main.py
```
