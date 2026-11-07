# B08　上下文管理器

> 示例：`examples/part_b/b08_context.py`

## 学完你能做什么

用 `with` 表达“进入时取得，离开时一定释放”，包括块里发生了异常的情况。

## 协议

`with obj` 调用 `obj.__enter__()`，把返回值绑到 `as` 后面的名字。离开块时，无论正常结束还是有异常，都调用 `__exit__(exc_type, exc, traceback)`。没有异常时这三个参数是 `None`。

`__exit__` 返回真值表示 **抑制** 这个异常，异常不会继续传播。返回假值或 `None` 表示不抑制。示例的 `Resource` 返回 `False`，所以 `RuntimeError` 仍然冒出来，但 `closed` 已经是 `True`。

不要为了“看起来处理过了”返回 `True`。抑制异常等于告诉调用方这块成功了。只有当你真的处理了这个异常、调用方不应该再看到它时才返回真值。文件对象的 `__exit__` 不会吞掉你的 `ValueError`。

## `contextmanager`

生成器加 `@contextmanager` 可以少写一个类。`yield` 之前是进入，`yield` 的值是 `as` 得到的对象，`yield` 之后是退出。退出代码放在 `finally` 里，这样有异常时也会执行。

```python
@contextmanager
def opened():
    state = {"open": True}
    try:
        yield state
    finally:
        state["open"] = False
```

`yield` 只能有一次。生成器在 `yield` 之后又产出，`contextmanager` 会报错。需要记住很多状态时，类比生成器清楚。

`contextlib` 里还有 `closing`、`suppress`、`nullcontext`。`suppress(FileNotFoundError)` 只吃掉你点名的异常。它比自己写一个返回 `True` 的 `__exit__` 更不容易扩大范围。

## 多个资源

可以写多行 `with`，或者在 3.10 及以后把多个上下文管理器放在括号里换行。后进入的先退出，和嵌套 `with` 一样。不要为了少缩进就把两个不相关的资源硬塞进一个生成器。

## 和异常章节的关系

`with` 就是把 `try` / `finally` 收成一个对象。A10 说过 `finally` 里不要 `return`。同样，`__exit__` 或 `contextmanager` 的 `finally` 里也不要 `return` 去替换原来的异常。释放资源，然后让原来的异常继续走。

## 常见错误

- `__enter__` 返回 `self`，调用方却以为 `as` 拿到了另一种对象。返回什么就在文档里写什么。锁的 `__enter__` 常常返回自己，文件的 `__enter__` 也返回自己。
- 在 `__exit__` 里做可能失败的第二次清理，又不处理。清理代码自己抛异常时，原来的异常会变成上下文。能简单就不要再添失败点。
- 自己调用 `__enter__` 而不调用 `__exit__`。用 `with`。

## 练习

1. 写一个上下文管理器，进入时把列表清空的动作推迟到退出时完成。退出后列表应为空。用类或 `contextmanager` 都可以。
2. 块里抛了 `RuntimeError`，怎样让它继续传播？
3. 什么时候选类，什么时候选 `contextmanager`？

参考答案：

1. `yield` 之后 `items.clear()`，并且写在 `finally` 里。
2. `__exit__` 返回 `False` 或 `None`。生成器版本不要在 `finally` 里吞掉异常。
3. 状态只是“进来、出去”两段时用 `contextmanager`。要给调用方一堆方法，或者生命周期里有多个字段时用类。

## 小结

`with` 保证 `__exit__` 被调用。返回真值才会吃掉异常，默认不要吃。`contextmanager` 用一次 `yield` 把进入和退出分开，清理放在 `finally`。
