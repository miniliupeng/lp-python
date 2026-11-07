"""题库 E02：描述符优先级、MRO 与不可哈希。"""

from __future__ import annotations


class Field:
    def __set_name__(self, owner: type, name: str) -> None:
        self.private = "_" + name

    def __get__(self, obj: object, objtype: type | None = None):
        if obj is None:
            return self
        return obj.__dict__.get(self.private)

    def __set__(self, obj: object, value: object) -> None:
        obj.__dict__[self.private] = value * 2


class Row:
    n = Field()

    def __init__(self, n: int) -> None:
        self.n = n


class A:
    def name(self) -> str:
        return "A"


class B(A):
    def name(self) -> str:
        return "B" + super().name()


class C(A):
    def name(self) -> str:
        return "C" + super().name()


class D(B, C):
    def name(self) -> str:
        return "D" + super().name()


def main() -> None:
    row = Row(3)
    assert row.n == 6
    assert [cls.__name__ for cls in D.__mro__[:4]] == ["D", "B", "C", "A"]
    assert D().name() == "DBCA"
    try:
        hash([])
    except TypeError:
        pass
    else:
        raise AssertionError("list 不可哈希")
    print("ok e02")


if __name__ == "__main__":
    main()
