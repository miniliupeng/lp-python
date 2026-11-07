# B07　dataclass 与枚举

> 示例：`examples/part_b/b07_dataclass_enum.py`

## 学完你能做什么

用 dataclass 表达一条记录，知道它什么时候能当字典键；用 `Enum` 表达一组固定取值，而不是散落的字符串。

## dataclass 生成什么

`@dataclass` 根据注解生成 `__init__`、`__repr__` 和 `__eq__`。你仍然可以自己写方法。它不是另一个类型系统，生成的是普通的类。

```python
@dataclass(frozen=True, slots=True)
class Point:
    x: int
    y: int
```

`frozen=True` 时，生成的类拒绝给字段赋值，并且因为相等性已经按字段定义、对象又不能改，dataclass 会生成 `__hash__`。示例里两个 `Point(1, 2)` 的哈希相同。

`slots=True` 让实例不再带 `__dict__`，属性写在固定的槽里，省内存，也防止随便挂新属性。`hasattr(Point(1, 2), "__dict__")` 为假。继承时，如果基类没有 `__slots__`，子类就算写了 `slots=True` 也仍然会从基类那里得到实例字典。要么整条链都规划槽，要么不要为了省那点内存去开槽。

## 默认可变字段

`items: list[str] = []` 这个写法 dataclass 会直接拒绝，因为那和函数的可变默认参数是同一个坑。正确写法是：

```python
items: list[str] = field(default_factory=list)
```

每个实例调用一次工厂，得到自己的列表。示例里往 `first.items` 追加，`second.items` 仍是空的。

## 比较了就会失去默认哈希

`@dataclass(eq=True)` 是默认行为。类可以变（没有 `frozen`）时，dataclass 把 `__hash__` 设为 `None`，实例不可哈希。示例对 `MutablePoint` 调用 `hash` 会得到 `TypeError`。

这是对的。可变且按内容比较的对象，放进集合之后再改字段，集合就坏了。如果你确定字段在当键期间不会变，可以 `unsafe_hash=True`，名字里的 unsafe 是认真的。多数业务对象不需要哈希，让它不可哈希即可。

`eq=False` 时不会生成相等方法，哈希保持对象默认的按身份哈希。很少需要这个组合。

## 枚举成员是单例

```python
class Color(Enum):
    RED = auto()
    BLUE = auto()
    CRIMSON = RED
```

`Color.RED is Color.CRIMSON`。相同的值做成了别名，不是第二个成员。遍历枚举时别名不会再出现一次。比较用 `is` 或 `==` 都可以，因为成员的相等就是身份。不要拿成员去和 `auto()` 背后的整数比，那些整数是实现分配的，不是你的 API。

需要和字符串配置文件互通时，用 `enum.StrEnum`（3.11 起）或者显式写出字符串值，并在边界上做一次转换。不要让 `"red"` 和 `Color.RED` 在整个程序里混用。边界上转一次，内部只用枚举。

`IntEnum` 的成员同时是整数，能参加算术。这很方便，也很容易把枚举漏回裸整数的世界。没有算术需求就用普通 `Enum`。

## 常见错误

- 给 dataclass 一个列表默认值，然后不理解为什么装饰器报错。用 `default_factory`。
- 把 `frozen` 理解成深冻结。字段本身如果是列表，列表里面仍能改。`frozen` 只是不许给字段重新赋值。
- 用 `Color.RED == 1` 判断颜色。把枚举当整数用，调用方就再也不会改成更合适的取值方式。

## 练习

1. 写一个冻结的 `Money(amount: Decimal, currency: str)`。金额用字符串构造 `Decimal`。
2. 两个空的 `Bag` 互不影响，靠的是哪一个参数？
3. `CRIMSON` 为什么不增加第三种颜色？

参考答案：

1. `@dataclass(frozen=True)`，字段类型分别是 `Decimal` 和 `str`。构造时写 `Decimal("1.20")`。
2. `field(default_factory=list)`。每个实例拿到新列表。
3. 它的值写成了 `RED`，枚举把它收成 `RED` 的别名，`is` 为真。

## 小结

dataclass 适合字段清楚的记录。可变且按字段比较的实例默认不能哈希；冻结之后可以。列表字段用工厂函数。枚举成员是单例，别名不会变成新成员。内部状态用枚举，字符串留在边界。
