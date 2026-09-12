# 专题 03：Python 3.11+ 结构化并发（TaskGroup）与 ExceptionGroup 异常传播

在早期的异步 Python 开发中，使用 `asyncio.gather()` 或手动创建后台 Task 常常引发严重的“**孤儿任务泄漏（Orphan Tasks）**”：当并发调用的其中一个子任务抛出异常失败时，其他正在后台运行的任务往往被遗忘并在后台继续浪费算力，甚至在服务退出后继续向被关闭的连接写入数据。Python 3.11+ 确立了现代 **结构化并发（Structured Concurrency via `asyncio.TaskGroup`）**。

---

## 一、 痛点驱动：非结构化并发的孤儿任务与异常吞噬

1. **孤儿任务后台脱缰**：
   - 发起两个并发网络操作 A 和 B。任务 A 抛出 500 错误立即向外冒泡，而任务 B 依然在后台无知无觉地跑了 10 分钟，白白耗费服务器 CPU 与数据库连接；
2. **多异常同时抛出的吞噬掩盖**：
   - 当多个并发任务同时崩溃时，传统的异常模型只能向外抛出其中“第一个”异常，导致其他并发任务的致命错误被彻底吞噬隐藏，极大增加故障排查难度。

---

## 二、 机制解密：结构化作用域（Lexical Scope）与异常树聚合

```text
[ asyncio.TaskGroup 结构化并发模型 ]
  async with asyncio.TaskGroup() as tg:
      tg.create_task(task_a())
      tg.create_task(task_b())
      tg.create_task(task_c())
         │
         ├─ 规则 1: 必须等待组内所有任务全部结束，上下文代码块才允许退出 (保证零孤儿)
         │
         └─ 规则 2: 若任务 A 抛出异常 ──> 自动向任务 B、C 发送 cancel() 级联取消信号！
                                      └──> 将全部异常聚合成 ExceptionGroup 一并抛出！
```

1. **严格的生命周期包裹（Structured Lifetime）**：
   - 保证任何子任务的生命周期绝不可能超出 `async with` 代码块的作用域；
2. **ExceptionGroup 与 except* 语法糖（PEP 654）**：
   - 允许一个异常容器包裹多个独立的异常树；
   - 引入 **`except* <ErrorType>:`** 语法，支持按照异常类型对并发抛出的多个异常进行解构与分别处理。

---

## 三、 生产规范与最佳实践

- **全面淘汰 `asyncio.gather()`**：新编写的生产微服务与批处理并发一律强制使用 `asyncio.TaskGroup`；
- **响应 CancelledError 优雅退出**：在长时间运行的协程中，遇到取消信号时必须正确清理局部资源并安全冒泡。
