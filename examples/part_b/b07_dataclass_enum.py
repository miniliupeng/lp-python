"""dataclass 的哈希规则与 Enum 身份。"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


@dataclass(frozen=True, slots=True)
class Point:
    x: int
    y: int


@dataclass(eq=True)
class MutablePoint:
    x: int
    y: int


@dataclass
class Bag:
    items: list[str] = field(default_factory=list)


class Color(Enum):
    RED = auto()
    BLUE = auto()
    CRIMSON = RED


def main() -> None:
    assert Point(1, 2) == Point(1, 2)
    assert hash(Point(1, 2)) == hash(Point(1, 2))
    assert not hasattr(Point(1, 2), "__dict__")
    try:
        hash(MutablePoint(1, 2))
    except TypeError:
        pass
    else:
        raise AssertionError("可比较且可变的数据类默认不可哈希")

    first = Bag()
    second = Bag()
    first.items.append("a")
    assert second.items == []

    assert Color.RED is Color.CRIMSON
    assert Color.RED is not Color.BLUE
    assert Color.RED != Color.BLUE
    print("ok b07")


if __name__ == "__main__":
    main()
