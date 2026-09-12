# 阶段 04: 面向对象、元编程与装饰器

面向对象与元编程是构建企业级框架与 SDK 的核心基石。本阶段剖析对象生命周期底层的实例化时序、魔术方法体系、描述符协议与多继承 C3 线性化算法，破译现代 Python 框架底层黑盒。

---

## 💡 核心工程心智与底层机制

1. **`__new__` vs `__init__` 对象生命周期**：
   - `__new__` 是真正的静态构造器，负责在堆内存申请并分配未初始化的对象实例指针；
   - `__init__` 是实例初始化方法，仅负责属性挂载；单例模式与不可变对象定制必须通过 `__new__` 拦截。
2. **核心魔术方法与富比较协议**：
   - 彻底区分 `__repr__`（面向开发者/无歧义）与 `__str__`（面向最终用户/可读性）；
   - 正确实现 `__eq__` 与 `__hash__` 协议，使自定义类能安全作为字典 Key 与集合元素。
3. **描述符协议（Descriptor Protocol）**：
   - 包含 `__get__`、`__set__` 与 `__delete__`；
   - 是 `@property`、`classmethod`、`staticmethod` 以及 ORM 字段校验的通用底层实现；资料描述符（Data Descriptor）优先级高于实例字典（`__dict__`）。
4. **企业级参数化装饰器**：
   - 熟练运用三层闭包结构编写高阶装饰器；
   - 严格使用 `functools.wraps` 保全被修饰函数的 `__name__`、`__doc__` 与签名元数据，杜绝可观测性与文档断裂。
5. **多重继承与 MRO C3 线性化算法**：
   - 彻底告别盲目的多继承与菱形继承陷阱；
   - 掌握通过 `super()` 驱动的确定性协作调用链与 C3 Linearization 单调拓扑排序。

---

## 🗺️ 阶段专题导航

| 专题目录 | 核心原语 | 关键掌握目标 |
| :--- | :--- | :--- |
| **[01-object-lifecycle-new-and-init](./01-object-lifecycle-new-and-init/)** | `__new__` 内存分配与时序 | 掌握实例内存分配、不可变对象构造拦截与企业级单例模式 |
| **[02-magic-methods-core](./02-magic-methods-core/)** | 核心魔术方法与富比较 | 深入 `__repr__`/`__str__`、`__eq__` 与可哈希性（Hashability） |
| **[03-property-and-descriptors](./03-property-and-descriptors/)** | 描述符协议与属性拦截 | 掌握资料/非资料描述符优先级、`@property` 原理与 ORM 映射基石 |
| **[04-decorators-engineering](./04-decorators-engineering/)** | 参数化装饰器与元信息保全 | 掌握高阶闭包时序、`functools.wraps`、执行耗时与异常统一重试 |
| **[05-oop-inheritance-and-mro](./05-oop-inheritance-and-mro/)** | 多重继承与 C3 算法 | 深入 MRO 拓扑排序、菱形继承协作链与 `super()` 生产防重入设计 |

---

## 🚀 统一运行验证

```bash
uv run python 04-oop-and-metaprogramming/01-object-lifecycle-new-and-init/main.py
uv run python 04-oop-and-metaprogramming/02-magic-methods-core/main.py
uv run python 04-oop-and-metaprogramming/03-property-and-descriptors/main.py
uv run python 04-oop-and-metaprogramming/04-decorators-engineering/main.py
uv run python 04-oop-and-metaprogramming/05-oop-inheritance-and-mro/main.py
```
