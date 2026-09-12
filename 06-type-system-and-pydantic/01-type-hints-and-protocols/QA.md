# 大厂高频面试题精讲 (05-01-type-hints-and-protocols)

---

### Q1: Python 的类型注解（Type Hints）在运行时会被强制执行吗？它对解释器性能有何影响？

#### 🎯 面试官考点
- 渐进式类型体系设计、元数据存储（`__annotations__`）与运行时擦除。

#### 💡 满分回答模板
1. **纯注解模式下的零强制性**：
   - 官方标准下，类型注解**完全不具备运行时强制约束力**；
   - 即使将声明为 `def add(x: int) -> int` 的函数传入字符串 `add("abc")`，CPython 虚拟机在运行时依然会正常执行拼接操作，绝不会自动抛出 `TypeError`；
   - 类型提示的主要价值在于供给开发期间的静态检查工具（MyPy, Pyright, IDE）进行代码门禁校验。
2. **运行时性能影响**：
   - **代码执行期零损耗**：编译为字节码后，所有类型注解完全不参与执行分发；
   - **模块加载期轻微开销**：在导入模块时，解释器会解析并把注解求值为元数据存入 `__annotations__` 字典；
   - **PEP 563 / PEP 649 演进**：通过 `from __future__ import annotations` 将类型注解转换为静态字符串存储（延迟求值），进一步消除了模块导入期对深层依赖类型的无谓解析。

---

### Q2: 简述 typing.Protocol（结构化类型）与 abc.ABC（标称类型）的本质区别。在设计插件系统时为何推荐 Protocol？

#### 🎯 面试官考点
- 标称子类型（Nominal Subtyping）vs 结构化子类型（Structural Subtyping）、面向接口编程演进。

#### 💡 满分回答模板
1. **核心本质区别**：
   - **`abc.ABC`（标称子类型，Nominal Typing）**：
     - 判定依据是**显式的“类血缘声明”**；实现类必须明确写明 `class MyService(BaseABC):`；
     - 缺点：侵入性强，无法将第三方库已有的现有类当作接口实现传递；
   - **`typing.Protocol`（结构化子类型，Structural Typing）**：
     - 判定依据是**对象的“形状与方法契约（Shape & Methods）”**；
     - 任何类只要实现了 Protocol 所声明的方法和签名，自动被认定为合法子类，**不需要任何显式继承**。
2. **插件系统为何推荐 Protocol**：
   - **完全解耦第三方生态**：插件作者不需要安装核心框架的 SDK 库去继承特定基类，只需实现约定方法即可即插即用；
   - **避免多继承钻石地狱**：消除了深层 ABC 继承树引发的 MRO 复杂性。

---

### Q3: 什么是 TypeVar 与泛型约束？如何在 Python 中表达支持任意类型的通用容器？

#### 🎯 面试官考点
- 参数化多态（Parametric Polymorphism）、类型变量（TypeVar）约束与边界。

#### 💡 满分回答模板
1. **TypeVar 的核心定位**：
   - 用于在函数入参和返回值之间建立**类型关联绑定**；
   - 如果不使用 TypeVar 而写 `def get_first(items: list[object]) -> object:`，外部调用后返回值将丢失具体类型推导；
   - 使用泛型：
     ```python
     from typing import TypeVar

     T = TypeVar("T")


     def get_first(items: list[T]) -> T:
         return items[0]
     ```
     静态分析器能精准推导出传入 `list[int]` 时返回值为 `int`。
2. **Python 3.12+ 现代 PEP 695 语法**：
   - 废弃了手写 `TypeVar` 的样板代码，原生支持在方括号中声明类型参数：
     ```python
     def get_first[T](items: list[T]) -> T:
         return items[0]
     ```
