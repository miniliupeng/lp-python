# 大厂高频面试题精讲 (03-03-property-and-descriptors)

---

### Q1: 请详述 Python 描述符协议（Descriptor Protocol）的核心三方法及其运行机制。

#### 🎯 面试官考点
- Python 属性查找核心机制（Attribute Lookup Scheme）、元编程控制权接管。

#### 💡 满分回答模板
1. **协议规范核心三方法**：
   - 任何实现了以下一个或多个方法的类，其创建的实例被挂载在其他类的类属性上时，即成为描述符：
     - **`__get__(self, instance, owner)`**：当通过 `obj.attr` 或 `Class.attr` 访问时触发；
     - **`__set__(self, instance, value)`**：当通过 `obj.attr = val` 赋值时触发；
     - **`__delete__(self, instance)`**：当通过 `del obj.attr` 删除属性时触发；
     - **`__set_name__(self, owner, name)`（Python 3.6+）**：类定义创建完成的瞬间，解释器自动回调该方法，把挂载的属性名称 `name` 注入给描述符。
2. **运行机制流转**：
   - 描述符必须被定义在**类属性（Class Attribute）**上，不能定义在实例级别；
   - 当外部执行属性点号操作时，解释器的属性访问分发引擎（`tp_getattro`）自动拦截请求，转发调用描述符对应的方法。

---

### Q2: 什么是数据描述符（Data Descriptor）与非数据描述符（Non-data Descriptor）？它们在实例属性字典中的查找优先级是怎样的？

#### 🎯 面试官考点
- 属性查找顺序的精确优先级规则（经典深挖八股）。

#### 💡 满分回答模板
1. **核心分类定义**：
   - **数据描述符（Data Descriptor）**：**定义了 `__set__()` 或 `__delete__()`** 的描述符（哪怕只定义了 `__set__` 并直接抛错）；
   - **非数据描述符（Non-data Descriptor）**：**仅定义了 `__get__()`** 而没有定义写方法的描述符（最典型的代表就是类的普通成员方法、`@staticmethod` 与 `@classmethod`）。
2. **实例属性查找绝对优先级（由高到低）**：
   1. **数据描述符（最高优先级！）**：只要类中挂载了数据描述符，就算实例自己的 `__dict__` 里有同名键，解释器也会**彻底无视实例自身字典，强制调用数据描述符的 `__get__`**！
   2. **实例自身字典（`instance.__dict__`）**：常规的动态属性、实例变量在此命中；
   3. **非数据描述符**：如果实例字典没有该键，才回退查找类中的非数据描述符；
   4. **类的普通属性**；
   5. **`__getattr__()` 兜底钩子**。

---

### Q3: @property 装饰器在底层的真实运作本质是什么？它与描述符有何内在联系？

#### 🎯 面试官考点
- 内置语法糖的底层还原、`property` 类的描述符本质。

#### 💡 满分回答模板
1. **本质还原**：
   - **`property` 本身就是一个完全遵循描述符协议的 C 语言内置类**；
   - `@property` 语法糖在底层完全等价于实例化了一个 `property` 描述符对象挂载在类属性上：
     ```python
     # 语法糖写法
     @property
     def age(self):
         return self._age


     # 底层等价还原
     def _get_age(self):
         return self._age


     age = property(fget=_get_age)
     ```
2. **数据描述符的身份确认**：
   - `property` 类在底层同时实现了 `__get__` 与 `__set__` 方法；
   - 即便用户只传了 `fget` 未定义 setter，它的 `__set__` 依然存在，并在被赋值时默认抛出 `AttributeError("can't set attribute")`。因此它是一个**绝对优先的数据描述符**。
