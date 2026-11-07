"""Protocol 做结构检查；边界上的解析函数拒绝坏输入。"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Greeter(Protocol):
    def greet(self) -> str: ...


class Person:
    def greet(self) -> str:
        return "hi"


def parse_port(text: str) -> int:
    port = int(text)
    if not 1 <= port <= 65535:
        raise ValueError("端口超出范围")
    return port


def main() -> None:
    assert isinstance(Person(), Greeter)
    assert parse_port("80") == 80
    try:
        parse_port("70000")
    except ValueError:
        pass
    else:
        raise AssertionError("越界端口应被拒绝")
    try:
        parse_port("http")
    except ValueError:
        pass
    else:
        raise AssertionError("非数字应被拒绝")
    print("ok d03")


if __name__ == "__main__":
    main()
