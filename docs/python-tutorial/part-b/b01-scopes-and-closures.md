# B01　参数、作用域与闭包

> 示例：`examples/part_b/b01_scopes.py`。可执行示例仍是 CPython 3.12。

## 学完你能做什么

读懂一个名字在函数里指的是谁，写出不会在调用之间串数据的默认参数，以及不会把循环变量漏给所有闭包的 lambda。

## LEGB

解析一个名字时，Python 按这个顺序找：

1. **L**ocal：当前函数的局部变量。
2. **E**nclosing：外层函数的局部变量，给闭包用。
3. **G**lobal：模块全局。
4. **B**uiltin：`len`、`print` 这些内置名字。

赋值默认把名字变成局部变量。函数里只要出现 `count = ...`，`count` 在整个函数里都是局部的，包括这一行之前的读取。那种“先读全局再赋值”会得到 `UnboundLocalError`，不是“前半段用全局”。

要在函数里给全局名字重新绑定，必须写 `global name`。要给外层函数的名字重新绑定，必须写 `nonlocal name`。只是读取外层变量时，两个声明都不要写。

`global` 和 `nonlocal` 都是重新绑定的开关，不是“把对象引进来”的开关。你很少需要 `global`。需要在闭包里累加计数时，`nonlocal` 是对的工具。

## 默认值只算一次

```python
def bad_append(item, bucket=[]):
    bucket.append(item)
    return bucket
```

`[]` 在定义函数时创建。之后每次省略 `bucket`，用的都是同一个列表。示例里连续两次调用会得到 `[1]` 然后 `[1, 2]`。这不是实现事故，语言就是这样规定的。

可变对象不要放在默认值里。用 `None` 当“调用方没传”的标记，在函数体内再创建新列表：

```python
def append_item(item: int, bucket: list[int] | None = None) -> list[int]:
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

如果 `None` 本身是合法业务值，就用一个模块级的哨兵对象：`MISSING = object()`，再用 `is` 判断。3.15 才有内置的 `sentinel` 类型，3.12 用 `object()` 即可。不要用某个“看起来不会出现的字符串”当哨兵。

## 闭包抓住的是名字

`make_multiplier` 返回的内部函数记住外层的 `factor`。这是你想要的闭包。

循环里写 `lambda: number` 时，每个 lambda 记住的是 **同一个** `number`。循环结束后它是最后一次的值，于是三个函数都返回 `2`。修法是在定义时把当前值绑进默认参数，默认参数在那时求值：

```python
funcs.append(lambda number=number: number)
```

示例把两种形态都跑了。默认参数这一写法是惯用法，不是技巧比赛。函数更长时，直接写 `def read(number=number)`，别挤在一行 lambda 里。

## `/` 和 `*`

3.8 起，参数列表里的 `/` 左边只能按位置传递，`*` 右边只能按关键字传递。

```python
def add(left: int, right: int, /) -> int:
    return left + right

def greet(*, name: str) -> str:
    return name
```

`add(left=1, right=2)` 抛 `TypeError`。这样可以保留以后改参数名的自由，调用方没有写成关键字。`greet` 强制写出 `name=`，调用点更不容易把参数传错位置。标准库里 `range`、`len` 很多参数都是位置仅限的，所以你不能写 `len(obj=items)`。

完整的合法顺序是：位置仅限参数、普通参数、`*args`、仅限关键字参数、`**kwargs`。入门阶段先把 `/` 和 `*` 的分界看懂，不必每次都写全。

## 常见错误

- 用可变默认值缓存结果，还觉得这是巧妙的记忆化。那是共享状态。记忆化用 `functools.cache`，见 B11。
- 在闭包里对循环变量只读，然后对结果感到惊讶。
- 给只需要读取的外层变量加 `nonlocal`。没有重新赋值就不需要它。

## 练习

1. 写 `make_adder(n)`，返回一个函数，把参数加上 `n`。
2. 解释为什么 `def f(x, items=[])` 在静态检查里会被标出来。示例对这一行使用了明确的忽略标记，只为了把坑跑给你看。
3. `def scale(value, /, *, factor)` 可以怎样调用，不可以怎样调用？

参考答案：

1. 内部函数 `return value + n`，返回这个内部函数。
2. 默认列表在定义时只创建一次，调用之间会共享。检查器在阻止这个坑。
3. `scale(3, factor=2)` 可以。`scale(value=3, factor=2)` 不行，因为 `value` 在 `/` 左边。`scale(3, 2)` 也不行，因为 `factor` 在 `*` 右边。

## 小结

名字按 LEGB 解析。默认值求值一次，所以列表不要做默认值。闭包绑定的是变量，循环里要用默认参数抓住当前值。`/` 和 `*` 把参数分成只能按位置、可混合、只能按关键字三段。
