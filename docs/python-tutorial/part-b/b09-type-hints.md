# B09　类型注解

> 示例：`examples/part_b/b09_typing.py`

## 学完你能做什么

给函数写 3.12 风格的注解，知道解释器不会按注解拒绝参数，并分清 3.12 和 3.14 在“注解什么时候求值”上的差别。

## 注解不是校验

```python
def double(number: int) -> int:
    return number * 2
```

示例调用 `double("ab")` 得到 `"abab"`。字符串可以乘整数，函数照做。注解没有插入检查代码。它服务三种读者：人、类型检查器（mypy、Pyright 等）、以及那些 **主动读取** 注解的库。

想在系统边界拒绝错误输入，要写解析函数或使用校验库，在边界上做一次。业务函数内部再写一遍 `isinstance`，通常是重复劳动。D03 把边界放在该放的地方。

## 3.12 默认会求值注解

在 3.12 里，函数定义执行到时，注解表达式会马上求值，结果放进 `__annotations__`。示例断言 `double.__annotations__["number"] is int`。所以注解里出现的名字那时必须已经存在，否则 `NameError`。

类体还没执行完时，类名自己还不能用。`Node` 的方法要引用 `Node`，3.12 把注解写成字符串：

```python
def __init__(self, nxt: "Node | None" = None) -> None:
    ...
```

这时 `__annotations__["nxt"]` 是字符串 `"Node | None"`。`typing.get_type_hints` 会在函数的全局命名空间里求值，得到真正的 `Node | None`。读别人注解的库应当走 `get_type_hints`（或 3.14 的 `annotationlib`），不要假设 `__annotations__` 里一定是类型对象。

`from __future__ import annotations` 在 3.12 会把注解推迟成字符串。这能解决前向引用，也会让所有 `__annotations__` 的值变成字符串。新代码如果同时要支持 3.12 和 3.14，不要假设某一种存储格式，用标准库的读取函数。

## 3.14 改成了延迟求值

PEP 649 和 PEP 749 从 3.14 起生效：函数、类和模块上的注解默认不再在定义时求值，而是存进 `__annotate__`，需要时才算。前向引用一般不用再加引号。`annotationlib.get_annotations` 可以选择：

- `VALUE`：求值成运行时的对象，接近旧行为。
- `FORWARDREF`：还没有的名字换成占位。
- `STRING`：得到字符串形式。

如果文件里仍然写了 `from __future__ import annotations`，行为另算，官方说明把这条路排除在“默认延迟”之外。3.12 的本教程示例不导入这条 future，也不调用 `annotationlib`，因为 3.12 没有这个模块。`examples/part_c/c07_version_probe.py` 会在 3.14 之前断言该模块不存在。

## 3.12 已经够用的写法

- 容器：`list[int]`、`dict[str, int]`、`tuple[int, ...]`。不要再写 `typing.List`。
- 可空：`int | None`。不要写 `Optional[int]`，除非你在维护旧代码。
- 类型别名：`type IntList = list[int]`（PEP 695）。它生成 `TypeAliasType`，示例检查了 `__value__`。
- 泛型函数同样用 PEP 695：`def first[T](items: list[T]) -> T`。
- 固定字面量用 `Literal["get", "post"]`。只用于类型检查器能利用的地方，运行时不会因此拒绝别的字符串。

`X | Y` 在运行时是 `types.UnionType`。它不等于运行时的 `isinstance` 自动支持一切组合。`isinstance(x, int | str)` 在 3.10 以上可以，但更复杂的注解，例如 `list[int]`，不能拿去 `isinstance`。运行时判断容器元素类型，要自己看元素。

## 常见错误

- 认为注解会让函数变慢一截。3.12 定义函数时会求值注解，这是定义期的成本，不是每次调用都重新解析源码。热点函数的成本几乎永远在函数体里。
- 在注解里做有副作用的调用。定义函数时它会执行。注解里只放类型表达式。
- 用字符串注解之后直接把它当类型去比较 `is int`。那是字符串。用 `get_type_hints`。

## 练习

1. 给 `clip(value, low, high)` 加上参数和返回值注解，全部是 `int`。
2. 为什么 `Node.__init__` 的注解在示例里是字符串，而 `double` 的不是？
3. 3.14 的延迟求值解决了哪个 3.12 的麻烦？

参考答案：

1. `def clip(value: int, low: int, high: int) -> int`。
2. `int` 在定义时已经存在，所以存的是 `int` 这个对象。`Node` 在类体里还不能引用，示例故意写成引号里的前向引用。
3. 注解里的前向引用通常不必再加引号，定义期也不必把每个注解都求值。读取方式改成 `annotationlib`。

## 小结

注解给人和工具看，调用时不自动校验。3.12 默认在定义时求值，前向引用常要写成字符串。3.14 起默认延迟求值，并用 `annotationlib` 读取。新代码用内置泛型和 `X | None`。
