"""参数、返回值和文档字符串。"""

from __future__ import annotations


def area(width: float, height: float = 1.0) -> float:
    """返回宽和高围成的矩形面积。"""
    return width * height


def scale(values: list[int], factor: int) -> list[int]:
    return [item * factor for item in values]


def main() -> None:
    assert area(3, 2) == 6
    assert area(3) == 3.0
    assert area(height=4, width=2) == 8
    doc = area.__doc__
    assert doc is not None and "矩形" in doc
    original = [1, 2]
    assert scale(original, 3) == [3, 6]
    assert original == [1, 2]
    print("ok a07")


if __name__ == "__main__":
    main()
