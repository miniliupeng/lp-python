"""装饰器、wraps，以及叠加顺序。"""

from __future__ import annotations

import functools


def counted(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return fn(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


def tag(label: str):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return (label, fn(*args, **kwargs))

        return wrapper

    return decorator


@counted
def inc(number: int) -> int:
    """加一。"""
    return number + 1


@tag("outer")
@tag("inner")
def value() -> int:
    return 1


def main() -> None:
    assert inc(3) == 4
    assert inc(4) == 5
    assert inc.calls == 2
    assert inc.__name__ == "inc"
    doc = inc.__doc__
    assert doc is not None and "加一" in doc
    assert value() == ("outer", ("inner", 1))
    print("ok b04")


if __name__ == "__main__":
    main()
