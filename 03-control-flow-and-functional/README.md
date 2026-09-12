# 阶段 03: 现代控制流与函数式编程

控制流是业务逻辑的心跳，而迭代器与生成器则是 Python 支撑高并发流处理与海量数据吞吐的底层引擎。本阶段覆盖 Python 3.10+ 最新模式匹配到生成器协程基石的演进全貌。

---

## 💡 核心工程心智与底层机制

1. **现代 Structural Pattern Matching（match-case）**：
   - Python 3.10 引入的 `match-case` 绝非简单的 switch-case 语法糖；
   - 具备运行时深层解构匹配（Destructuring）、类模式绑定与 `if` 模式守卫，是消除恶性 `if-elif-else` 嵌套的利器。
2. **函数一等公民与闭包作用域**：
   - 彻底掌握 CPython 作用域四层查找链：**LEGB**（Local $\to$ Enclosing $\to$ Global $\to$ Built-in）；
   - 深刻理解闭包底层 `__closure__` 与 `cell` 对象的自由变量绑定机制。
3. **迭代器协议底层规范**：
   - 实现 `__iter__()`（返回迭代器自身）与 `__next__()`（递进状态并在终止时抛出 `StopIteration`）；
   - 掌握常数级 $O(1)$ 内存开销的惰性流式计算范式，规避海量数据集撑爆内存。
4. **生成器状态机与双向协程管道**：
   - 生成器函数编译后生成生成器代码对象，挂起时保存堆栈帧（Frame Object）上下文；
   - 掌握通过 `yield` 暂停、`send()` 注入数据、`close()` 与 `throw()` 实现的原生双向管道协作。

---

## 🗺️ 阶段专题导航

| 专题目录 | 核心原语 | 关键掌握目标 |
| :--- | :--- | :--- |
| **[01-modern-pattern-matching](./01-modern-pattern-matching/)** | 结构化模式匹配与解构 | 掌握序列解构、字典提取、类模式匹配与 guard 守卫过滤 |
| **[02-functions-signatures-and-scopes](./02-functions-signatures-and-scopes/)** | LEGB 作用域与闭包 | 深入函数作为一等公民、闭包自由变量捕获机制与作用域修饰 |
| **[03-iterators-protocol](./03-iterators-protocol/)** | 迭代器协议与惰性序列 | 彻底吃透 `__iter__` 与 `__next__`，掌握大数据流式 $O(1)$ 内存计算 |
| **[04-generators-and-coroutines](./04-generators-and-coroutines/)** | 生成器状态机与 send 管道 | 掌握 `yield` 暂停恢复、`send()` 双向交互与事件驱动协程原语 |

---

## 🚀 统一运行验证

```bash
uv run python 03-control-flow-and-functional/01-modern-pattern-matching/main.py
uv run python 03-control-flow-and-functional/02-functions-signatures-and-scopes/main.py
uv run python 03-control-flow-and-functional/03-iterators-protocol/main.py
uv run python 03-control-flow-and-functional/04-generators-and-coroutines/main.py
```
