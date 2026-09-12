# 大厂高频面试题精讲 (04-03-structured-concurrency-taskgroup)

---

### Q1: 什么是结构化并发（Structured Concurrency）？相比传统的 asyncio.gather()，asyncio.TaskGroup 解决了什么痛点？

#### 🎯 面试官考点
- 并发编程范式演进、线程/任务泄漏防御（Leak Prevention）与生命周期约束。

#### 💡 满分回答模板
1. **结构化并发的核心哲学**：
   - 借鉴自结构化编程（如 if/for/while 代码块具有明确入口和出口）；
   - **铁律**：**任何并发任务的生命周期，绝不能逃逸出创建它的词法作用域（Lexical Scope）**。当代码离开当前控制块时，必须确保所有并发子任务已全部终结。
2. **传统 `asyncio.gather()` 的严重痛点**：
   - **孤儿任务无声泄漏（Orphan Tasks）**：默认情况下，当 `gather` 中的某一个任务崩溃抛错时，`gather` 立即向外抛出异常，**但其他正在运行的任务并不会被自动停止**，它们在后台脱缰运行，可能继续修改已关闭的数据库连接造成脏写；
   - **必须手动写繁琐的取消代码**：过去为了防止泄漏，必须手动循环遍历任务并逐一调用 `t.cancel()`，代码极易出现疏漏。
3. **`TaskGroup` 的解决机制**：
   - 通过 `async with asyncio.TaskGroup() as tg:` 上下文管理；
   - 任何一个任务出错，**TaskGroup 自动向组内所有正在运行的剩余任务立即广播 `cancel()` 取消信号**，并且保证在上下文退出前等待所有任务完全退出，做到 100% 零孤儿任务。

---

### Q2: 什么是 ExceptionGroup？在 Python 3.11+ 中如何使用 except* 语法优雅捕获并处理多个并发异常？

#### 🎯 面试官考点
- PEP 654 异常树（Exception Groups）机制、`except*` 语法糖的解包模式。

#### 💡 满分回答模板
1. **产生背景**：
   - 在并发编程中，3 个并发任务可能同时抛出不同的异常（如一个抛出 `TimeoutError`，另一个抛出 `ValueError`）；
   - 传统的 Python 异常模型只能向外抛出单一异常，强行二选一会直接导致另一个异常丢失；
   - Python 3.11+ 引入 **`ExceptionGroup`**，它是一个可以像树状结构一样嵌套容纳多个异常的容器类。
2. **`except*` 语法糖运行机制**：
   - 使用 **`except* <Type> as eg:`** 可以对异常组进行**分流解构匹配**：
     ```python
     try:
         async with asyncio.TaskGroup() as tg:
             ...
     except* TimeoutError as eg:
         # 仅提取处理异常组中的所有超时异常
         logger.warning("处理超时任务: %s", eg.exceptions)
     except* ValueError as eg:
         # 剩余的参数错误异常在此处被分别处理
         logger.error("处理非法参数: %s", eg.exceptions)
     ```
   - 每一个 `except*` 分支只提取它关心的子异常，未被匹配的异常会继续作为一个子异常组向上冒泡，彻底解决了多异常并发捕获与分类治理难题。
