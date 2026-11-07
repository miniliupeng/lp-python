"""作用域、默认参数、闭包迟绑定，以及 / 与 *。"""

from __future__ import annotations


def make_multiplier(factor: int):
    def multiply(value: int) -> int:
        return value * factor

    return multiply


def append_item(item: int, bucket: list[int] | None = None) -> list[int]:
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


def bad_append(item: int, bucket: list[int] = []) -> list[int]:  # noqa: B006
    """演示共享默认列表。新代码不要这样写。"""
    bucket.append(item)
    return bucket


def late_binding() -> list[int]:
    funcs = []
    for number in range(3):
        funcs.append(lambda number=number: number)
    return [fn() for fn in funcs]


def broken_late_binding() -> list[int]:
    funcs = []
    for number in range(3):
        funcs.append(lambda number=number: number)
    # 正确写法已经用默认参数绑住循环变量。下面单独展示错误形态。
    wrong = []
    for number in range(3):

        def read(number: int = number) -> int:
            return number

        wrong.append(read)
    assert [fn() for fn in wrong] == [0, 1, 2]
    leaked: list = []
    for number in range(3):
        leaked.append(lambda: number)  # noqa: B023
    return [fn() for fn in leaked]


def add(left: int, right: int, /) -> int:
    return left + right


def greet(*, name: str) -> str:
    return name


def main() -> None:
    assert make_multiplier(3)(4) == 12
    assert append_item(1) == [1]
    assert append_item(2) == [2]
    shared: list[int] = []
    append_item(1, shared)
    append_item(2, shared)
    assert shared == [1, 2]

    assert bad_append(1) == [1]
    assert bad_append(2) == [1, 2]

    assert late_binding() == [0, 1, 2]
    assert broken_late_binding() == [2, 2, 2]

    assert add(1, 2) == 3
    try:
        add(left=1, right=2)  # type: ignore[misc]
    except TypeError:
        pass
    else:
        raise AssertionError("位置仅限参数不能用关键字")
    assert greet(name="Ada") == "Ada"
    print("ok b01")


if __name__ == "__main__":
    main()
