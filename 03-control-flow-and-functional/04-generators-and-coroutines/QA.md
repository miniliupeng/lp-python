# 大厂高频面试题精讲 (02-04-generators-and-coroutines)

---

### Q1: 为什么在处理海量数据或日志流时，必须优先使用生成器而非列表推导式？

#### 🎯 面试官考点
- 内存复杂度分析（O(1) 恒定流式 vs O(N) 瞬时堆暴涨）、流式管道架构设计。

#### 💡 满分回答模板
1. **求值时序与内存消耗的本质不同**：
   - **列表推导式（List Comprehension，`[x for x in data]`）**：采用**及早求值（Eager Evaluation）**。它在表达式解析完毕的瞬间，在堆内存中完整分配一个容纳全量数据的列表对象。当数据量达到千万级时，直接引发严重的操作系统虚拟内存分页甚至触发 OOM-Killer；
   - **生成器表达式（Generator Expression，`(x for x in data)`）**：采用**惰性求值（Lazy Evaluation）**。调用时仅返回一个只有几十字节大小的生成器对象，只有下游迭代消费到某一项时才就地计算该项，全生命周期保持 **O(1) 恒定内存占用**。
2. **流水线链式处理（Pipeline Streaming）**：
   - 多个生成器可以通过串行组合构成流式管道：
     ```python
     lines = (line for line in open("huge.log"))
     errs = (l for l in lines if "ERROR" in l)
     data = (json.loads(l) for l in errs)
     ```
   - 整个链路不需要任何全局临时文件或中间大数组缓冲，数据像流水一样在各阶段平滑流过，架构吞吐量与稳定性极佳。

---

### Q2: 请详述生成器底层的运行机制。yield 是如何在 CPython 堆栈帧中挂起并保留局部变量状态的？

#### 🎯 面试官考点
- CPython C 源码实现、执行栈帧（PyFrameObject）、字节码指针（f_lasti）与代码对象生成器标记。

#### 💡 满分回答模板
1. **代码对象的静态标记（CO_GENERATOR）**：
   - 当函数体内包含 `yield` 关键字时，编译器在编译期就会为该函数的代码对象（`co_flags`）标记上 **`CO_GENERATOR`** 标志；
   - 运行时当调用该函数时，解释器检测到该标志，**不会立即执行任何函数体代码**，而是直接创建一个 **`PyGenObject`** 结构体返回。
2. **栈帧对象的堆分配与冻结挂起**：
   - 普通函数执行时，其 `PyFrameObject` 随着函数返回而被弹出并销毁；
   - 生成器不同：`PyGenObject` 结构体内部直接持有了指向独立栈帧的指针；
   - 当执行遇到 **`YIELD_VALUE`** 字节码时：
     1. 解释器将栈顶的值返回给外部调用方；
     2. 将当前虚拟机的指令计数器（`f_lasti`）精准保存在栈帧中，将生成器状态置为 **`GEN_SUSPENDED`**；
     3. 退出执行循环，但不释放该帧对象及其局部变量字典；
   - 下次外部调用 `next()` 时，解释器取出被挂起的帧对象，直接跳转到 `f_lasti + 1` 处无缝恢复现场继续执行。

---

### Q3: yield from 语法糖底层到底完成了哪些复杂工作？它与纯粹的 for x in subgen: yield x 有何区别？

#### 🎯 面试官考点
- PEP 380 委托生成器（Delegating Generator）协议、双向通道透传与返回值捕获。

#### 💡 满分回答模板
1. **双向异常与数据通道（Full Bi-directional Channel）**：
   - 如果仅仅写 `for x in subgen: yield x`，外部调用方对当前生成器调用 **`send()`**、**`throw()`** 或 **`close()`** 时，信号只能被外层捕获，**根本无法穿透传递给内部的子生成器 `subgen`**；
   - **`yield from`** 在外部调用方与最内层子生成器之间建立了一条**完全透明的双向直连通道**：外部调用 `send()` 传入的值会直接注入子生成器，子生成器抛出的异常会原样向外透传，反之亦然。
2. **自动捕获子生成器的最终返回值**：
   - 在 Python 3 中，生成器内部允许写 `return "finished"`（该返回值保存在抛出的 `StopIteration(value)` 异常中）；
   - 简单的 `for` 循环会直接丢弃该返回值；
   - 而 `result = yield from subgen` **能够自动捕获子生成器 `return` 的值并安全赋给变量 `result`**，这构成了早期没有 `async/await` 前原生协程框架（如 Python 3.4 asyncio）的执行引擎基础。
