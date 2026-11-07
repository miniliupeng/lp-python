# A10　错误与异常

> 示例：`examples/part_a/a10_exceptions.py`

## 学完你能做什么

按层次捕获异常，保留原因链，并且不在 `finally` 里偷偷换掉返回值。

## 异常是对象

`raise DomainError(text)` 创建一个异常对象并开始栈展开。调用栈上如果没有匹配的 `except`，程序退出并打印回溯。回溯是诊断信息，不是需要消灭的噪音。库的边界上把异常转成用户能理解的结果；调试时先读回溯。

捕获：

```python
try:
    return int(text)
except ValueError as exc:
    raise DomainError(text) from exc
```

`except ValueError` 只接这一支，包括它的子类。捕获太宽会把编程错误一起吞掉。

## 层次

```text
BaseException
├── KeyboardInterrupt
├── SystemExit
├── GeneratorExit
└── Exception
    ├── ValueError
    ├── TypeError
    ├── KeyError
    ├── RuntimeError
    └── ... 绝大多数业务和库异常
```

平时写的 `except Exception` 接的是 `Exception` 这一支。`KeyboardInterrupt`、`SystemExit`、`GeneratorExit` 不在其中。示例故意抛出 `KeyboardInterrupt` 再接住，用来说明 `isinstance(exc, Exception)` 为假。

因此：

- 不要写裸 `except:`。它连中断和系统退出一起吞。
- `except Exception` 是“记录下来并继续”时的宽捕获，仍然不该到处都是。能写具体类型就写具体类型。
- 生成器和异步任务里的 `GeneratorExit`、`CancelledError` 也是 `BaseException` 的子孙（`CancelledError` 从 3.8 起不再继承 `Exception`）。吞掉它们会让取消失效。C06 再讲取消。

3.11 起还有 `ExceptionGroup` 和 `except*`，用来一次抛出或捕获一组异常。入门阶段先把单个异常写对。你看到 `except*` 时，知道它是另一条语法，普通 `except` 不会拆开异常组。

## `raise from` 与异常链

`raise DomainError(text) from exc` 把原来的 `ValueError` 放进 `__cause__`。打印时你会看到“在处理这个异常时，另一个异常发生了”的明确原因。直接 `raise DomainError` 也会把正在处理的异常放进 `__context__`，但 `from` 表示你承认这是原因。

`raise DomainError from None` 抑制上下文的显示，只在原来的异常确实没有诊断价值时使用。不要为了输出好看把原因丢掉。

## `else` 和 `finally`

执行顺序：

1. `try`。
2. 若有匹配异常，`except`。
3. 若没有异常，`else`。
4. 无论是否发生异常，`finally`。

`finally` 用来释放资源。如果 `finally` 里又写了 `return` 或 `raise`，它会取代 `try` 里准备好的返回值或异常。示例里 `finally_wins` 的 `try` 要返回 `1`，`finally` 返回 `2`，调用方得到 `2`。原来的返回值消失。

这在 3.12 是合法且危险的。3.14 起（PEP 765），`return` / `break` / `continue` 如果会离开 `finally`，编译器发出 `SyntaxWarning`。警告不是从 3.12 就有的，所以旧代码不会自动提醒你。新代码不要在 `finally` 里 `return`。

## 自定义异常

继承 `Exception`，名字以 `Error` 结尾。在里面放调用方需要的字段，不要只塞一段已经格式化好的句子。示例的 `DomainError` 很薄，真实代码至少会保留非法的输入值。

不要继承 `BaseException`，除非你在写和 `SystemExit` 同级的控制流信号。普通错误不是信号。

## 常见错误

- `except Exception: pass`。失败被抹掉，后面用到半初始化的数据，错误更难查。
- 捕获 `Exception` 之后不记录也不重新抛出。
- 用异常的字符串内容做分支。捕获类型，读属性。字符串会变。

## 练习

1. 写 `positive(n)`，`n <= 0` 时抛 `ValueError`。
2. 调用 `positive(0)`，捕获后断言异常类型，不要断言整段英文句子。
3. 说明为什么示例必须用 `except BaseException` 才能看到 `KeyboardInterrupt`。

参考答案：

1. `if n <= 0: raise ValueError(n)`，否则 `return n`。
2. `except ValueError as exc`，再 `assert exc.args[0] == 0` 或只断言类型。
3. `KeyboardInterrupt` 的基类是 `BaseException` 不是 `Exception`。`except Exception` 接不住它，它会继续往外走，通常表现为程序被中断。

## 小结

捕获具体类型。原因用 `raise ... from`。`finally` 做清理，不写 `return`。`Exception` 和 `BaseException` 的分界决定了中断、退出和取消能不能生效。
