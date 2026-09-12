# 专题 03：描述符协议（__get__ 与 __set__）与 ORM 字段拦截底层

在 Python 框架开发中，**描述符（Descriptors）**是整个语言最为强大的属性访问黑魔法。从最常用的 `@property` 属性装饰器、`@classmethod`、`@staticmethod`，到大型 ORM（如 SQLAlchemy、Django ORM）的模型字段类型强校验，其底层全部建立在统一的**描述符协议（Descriptor Protocol）**之上。

---

## 一、 痛点驱动：样板代码爆炸与字段校验逻辑割裂

在编写大型业务实体模型时：
```python
class Order:
    def __init__(self, price, quantity):
        if not isinstance(price, float) or price < 0:
            raise ValueError(...)
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError(...)
        self._price = price
        self._quantity = quantity
```
若实体有数十个字段，每个类都要写大量重复的 `@property` 存取器与类型检查逻辑。系统需要一种能够**跨类复用、声明式拦截属性读写**的高级元编程原语。

---

## 二、 机制解密：描述符协议与实例 __dict__ 查找优先级

```text
实例属性访问 obj.attribute 的底层判定拓扑:
  1. 查找 obj 所属类及其 MRO 继承链
         │
         ├─ 发现“数据描述符” (实现了 __set__ 或 __delete__)
         │     └──> 具有最高绝对优先级！直接调用 Descriptor.__get__(instance, owner)
         │
         ├─ 否则查找实例自身的 __dict__ 属性字典 (obj.__dict__['attribute'])
         │     └──> 若存在，直接返回实例字典中的值！
         │
         ├─ 否则查找“非数据描述符” (仅实现了 __get__，如普通方法、静态方法)
         │     └──> 调用 Descriptor.__get__(instance, owner)
         │
         └─ 若上述皆未命中 ──> 最终触发类中的 __getattr__() 兜底抛出 AttributeError
```

1. **三方法协议标准**：
   - **`__get__(self, instance, owner)`**：获取属性时触发；
   - **`__set__(self, instance, value)`**：赋值拦截时触发（使该描述符成为“数据描述符”）；
   - **`__delete__(self, instance)`**：删除属性拦截；
2. **存储隔离核心原则**：
   - 描述符实例定义在**类级别**（所有实例共享同一个描述符对象）；因此保存各实例的属性值时，必须将数据保存在各实例自身的 `__dict__` 中，否则会导致所有实例的属性被串扰覆写！

---

## 三、 生产规范与最佳实践

- **利用 `__set_name__` 自动获取字段名（Python 3.6+）**：避免在构造器中手工传属性名字符串；
- **只读字段控制**：实现 `__set__` 并在其内部抛出 `AttributeError("Can't set attribute")` 即可构筑防篡改安全属性。
