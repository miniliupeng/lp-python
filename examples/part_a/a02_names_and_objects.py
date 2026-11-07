"""赋值绑定名字；类型跟对象走，运算不做隐式字符串转换。"""

from __future__ import annotations


def main() -> None:
    shared = [1]
    alias = shared
    alias.append(2)
    assert shared == [1, 2]
    assert shared is alias

    left = 1
    right = left
    left = 2
    assert right == 1

    value: object = 1
    value = "one"
    assert value == "one"

    try:
        _ = "1" + 1  # type: ignore[operator]
    except TypeError:
        pass
    else:
        raise AssertionError("str 与 int 不能相加")

    assert type(1) is int  # noqa: UP003
    assert isinstance(True, int)
    print("ok a02")


if __name__ == "__main__":
    main()
