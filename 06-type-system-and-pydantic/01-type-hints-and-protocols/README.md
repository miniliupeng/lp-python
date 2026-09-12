# 专题 01：现代类型提示、泛型与 typing.Protocol 结构化契约

Python 虽然是一门动态类型语言，但在超大型工程与复杂微服务架构中，缺乏类型约束会导致“重构即毁灭”。从 PEP 484 到现代 Python 3.10+ 原生类型语法（`int | str`, `list[T]`），Python 建立了成熟的**渐进式类型系统（Gradual Typing）**。深入理解基于 **`typing.Protocol` 的结构化子类型（鸭子类型规范化）**，是实现高内聚、低耦合架构设计的关键。

---

## 一、 痛点驱动：标称继承（Nominal Typing）的侵入性强耦合

在传统面向对象中，为了保证多态，通常强制依赖抽象基类：
```python
from abc import ABC, abstractmethod


class PaymentService(ABC): ...


class MockPayment(PaymentService): ...  # ❌ 必须强行继承抽象基类
```
如果接入第三方外部库（无法修改其源码继承自己的基类），传统的抽象类继承就会彻底破裂；且深层继承树会带来脆弱的紧耦合。

---

## 二、 机制解密：标称子类型 vs 结构化子类型（Protocol）

```text
[ 标称子类型 (Nominal Typing via ABC) ]
  判定依据: 显式声明的继承血缘关系 (Class A 必须显式继承 Class B)
  缺点: 侵入性极强，无法适配未直接继承的第三方库

[ 结构化子类型 (Structural Typing via typing.Protocol) ]
  判定依据: 检查对象的“形状 (Shape)”与具备的方法/属性
  哲学: 真正的 Pythonic 鸭子类型静态化 —— “走起来像鸭子、叫起来像鸭子，就是鸭子”
```

1. **`typing.Protocol` 的运行原理（PEP 544）**：
   - 任何类只要**实现了 Protocol 中声明的方法签名**，静态类型检查器（MyPy, Pyright）就会自动判定该类是该 Protocol 的合法子类型，**无需任何显式继承声明**；
2. **`@runtime_checkable` 增强**：
   - 允许在运行时使用 `isinstance(obj, MyProtocol)` 对对象的结构与方法进行动态反射探针。

---

## 三、 生产规范与最佳实践

- **优先推崇组合与协议（Protocols over Inheritance）**：定义业务依赖时，尽量使用小而专一的 Protocol（如 `ReaderProtocol`, `WriterProtocol`）；
- **拥抱现代 PEP 604 联合类型**：使用 `int | None` 替代历史冗长的 `Optional[int]`。
