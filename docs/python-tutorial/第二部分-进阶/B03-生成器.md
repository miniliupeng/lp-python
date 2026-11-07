# B03　生成器

> 示例：`examples/part_b/b03_generators.py`

## 学完你能做什么

用 `yield` 写出惰性序列，用 `send` 往生成器里送值，并知道 `close` 之后不能再推进。

## `yield` 把函数变成生成器

函数体里出现 `yield`，调用这个函数 **不会执行函数体**，而是返回一个生成器对象。真正执行到 `yield` 是在第一次 `next` 或 `for` 的时候。`yield` 把值交给调用方，同时把函数的局部状态冻在这一行。下次 `next` 从这行之后继续。

这和“返回一个列表”不同。列表把所有元素放在内存里。生成器一次只产出一个，适合大文件、网络流、无限序列。无限序列不能 `list()` 它。

示例的 `countdown` 从 `start` 往下产出。`yield start` 的结果可以接收调用方送进来的值。第一次只能 `next`（或 `send(None)`），因为还没有任何 `yield` 在等待接收。

## `send`

```python
received = yield start
```

`next(gen)` 等价于 `gen.send(None)`。`gen.send(5)` 让这次 `yield` 表达式的值变成 `5`，生成器据此把 `start` 改成 `5`，再产出新的当前值。

`send` 是协程的前身。现代异步代码用 `async`/`await`，不要用生成器硬写一套异步框架。`send` 仍然适合“管道中间可以接受控制指令”这种同步场景。指令一复杂，就改成普通的类，状态会更好读。

## `yield from`

`yield from iterable` 把另一个可迭代对象的元素逐个交出去，直到它结束。示例的 `chain` 先交出 `(1, 2)`，再交出 `(3,)`。调用方看到的是平坦的 `1, 2, 3`。

`yield from` 也会把 `send` 和 `throw` 转给子生成器。你只是在拼接序列时，可以把它理解成一个省事的循环。子生成器如果 `return` 了一个值，`yield from` 表达式的值就是那个返回值。这是 `yield from` 比手写 `for` 多出来的部分。

## `close` 和 `throw`

`close()` 在生成器暂停的 `yield` 处抛出 `GeneratorExit`。生成器应当结束，不要再 `yield`。再 `yield` 会变成 `RuntimeError`。`GeneratorExit` 继承 `BaseException`，不继承 `Exception`，所以 `except Exception` 接不住它。清理资源放在 `finally` 里，`finally` 里不要再 `yield`。

示例在 `send` 之后调用 `close()`，再 `next` 会得到 `StopIteration`。不要在 `finally` 里 `return` 去“返回关闭原因”：那会替换掉正在传播的 `GeneratorExit`，3.14 还会对离开 `finally` 的 `return` 给出 `SyntaxWarning`（PEP 765）。A10 已经演示过 `finally` 里 `return` 的后果，这里不再复制那种写法。

`throw(exc)` 在暂停点抛出一个你指定的异常。生成器可以捕获它并继续，也可以让它冒出去。测试里用它注入失败；业务代码更常见的是直接 `close`。

## 常见错误

- 调用生成器函数时期望它马上算完。它只是把生成器对象交给你。
- 在生成器里 `raise StopIteration`。用 `return`。
- 把一个生成器交给两个循环。第二个什么都得不到。

## 练习

1. 写 `positive(numbers)`，只 `yield` 大于 0 的数。
2. 用 `yield from` 把两个列表接成一个生成器。
3. 为什么第一次推进要用 `next`，不能直接 `send(1)`？

参考答案：

1. `for n in numbers: if n > 0: yield n`。
2. 两个 `yield from` 分别对两个列表。
3. 生成器要先执行到第一个 `yield`，才有地方接收送进去的值。第一次 `send` 只允许 `None`。

## 小结

`yield` 暂停函数并交出一个值。`send` 把值送回暂停点。`yield from` 委托给另一个迭代器。`close` 用 `GeneratorExit` 要求生成器停下来，这个异常不要被宽泛的 `except Exception` 吃掉。
