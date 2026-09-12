# 大厂高频面试题精讲 (02-02-functions-signatures-and-scopes)

---

### Q1: 简述 Python 函数签名中 /（位置专用）与 *（关键字专用）的语法规则与设计意图。

#### 🎯 面试官考点
- PEP 570 / PEP 3102 规范理解、API 演化稳定性与向后兼容性（Backward Compatibility）。

#### 💡 满分回答模板
1. **语法规则**：
   - **`/`（Positional-only Parameter Marker）**：位于 `/` 左侧的所有形参，调用方**只能通过位置传递**，严禁使用关键字形参名（如 `f(1)` 合法，`f(x=1)` 报错）；
   - **`*`（Keyword-only Parameter Marker）**：位于 `*` 右侧的所有形参，调用方**只能通过显式关键字传递**（如 `f(flag=True)` 合法，`f(True)` 报错）。
2. **架构设计意图**：
   - **解耦内部实现与外部契约（`/` 的价值）**：库开发者未来重构代码修改参数名（如将 `x` 改为 `coordinate_x`），调用方代码完全无感知，消除了无意的破坏性变更（Breaking Change）；
   - **消除歧义调用，增强可读性（`*` 的价值）**：防止多布尔值参数连传（如 `create_user("Tom", True, False, True)` 根本无法阅读），强制写成 `create_user("Tom", is_admin=True, send_email=False)`。

---

### Q2: 请详述 Python 变量解析的 LEGB 规则，以及 global 与 nonlocal 关键字的底层区别。

#### 🎯 面试官考点
- CPython 符号表解析、静态作用域、嵌套词法环境（Lexical Scope）状态操作。

#### 💡 满分回答模板
1. **LEGB 搜索时序**：
   - 解释器在查找一个变量时，严格按照单向顺序搜索：
     - **L (Local)**：当前函数最内层的局部作用域；
     - **E (Enclosing)**：外部嵌套函数的闭包作用域（从内向外逐层查找）；
     - **G (Global)**：当前模块文件的全局命名空间；
     - **B (Built-in)**：Python 内置模块（如 `len`, `range`）。
2. **`global` vs `nonlocal` 本质区别**：
   - **`global`**：声明该变量直接绑定到**模块级 Global 命名空间**。无论嵌套在多少层函数中，赋值都会修改模块最外层变量；
   - **`nonlocal`（Python 3 引入）**：声明该变量绑定到**最近一层的外部封闭闭包（Enclosing）作用域**，明确禁止在当前函数新建局部同名变量，但**绝不搜索 Global 和 Built-in**；
   - **无声明时的默认规则**：在函数内只要存在对变量的赋值操作（`x = ...`），Python 编译器会在编译期直接将 `x` 标记为 Local。如果之前没有赋值就读取，会直接抛出 `UnboundLocalError`。

---

### Q3: 什么是“闭包延迟绑定（Late Binding）”陷阱？底层成因是什么？如何优雅解决？

#### 🎯 面试官考点
- 闭包作用域环境模型、函数编译字节码对 Free Variables 的间接指针引用。

#### 💡 满分回答模板
1. **现象与底层成因**：
   - 当在循环体中创建函数（例如 `funcs = [lambda: i for i in range(3)]`）并后续执行时，所有函数返回的都是 `2`；
   - **底层成因**：Python 闭包在创建时，**并不会对引用的自由变量（Free Variable）进行即时值拷贝**，而是在其内部结构体通过一个 Cell 对象保存了对外部变量 `i` 符号地址的指针；
   - 当循环结束时，变量 `i` 的最终值停留在 `2`。当后续调用闭包时，它们通过指针在同一作用域检索到的都是最新的终态值 `2`。
2. **标准生产解法**：
   - **默认参数就地捕获法（最推荐、最 Pythonic）**：
     ```python
     funcs = [lambda x=i: x for i in range(3)]
     ```
     原理：函数默认参数在**函数定义（循环推进）的瞬间被求值并固化入函数的 `__defaults__`**，成功将每次遍历的快照即时锁定；
   - **`functools.partial` 偏函数法**：
     ```python
     from functools import partial

     funcs = [partial(lambda x: x, i) for i in range(3)]
     ```
