"""继承、super 与 C3 MRO。"""

from __future__ import annotations


class Animal:
    def speak(self) -> str:
        return "..."


class Dog(Animal):
    def speak(self) -> str:
        return "woof" + super().speak()


class A:
    def ping(self) -> str:
        return "A"


class B(A):
    def ping(self) -> str:
        return "B" + super().ping()


class C(A):
    def ping(self) -> str:
        return "C" + super().ping()


class D(B, C):
    def ping(self) -> str:
        return "D" + super().ping()


def main() -> None:
    assert Dog().speak() == "woof..."
    assert D().ping() == "DBCA"
    assert [cls.__name__ for cls in D.__mro__] == ["D", "B", "C", "A", "object"]
    print("ok b05")


if __name__ == "__main__":
    main()
