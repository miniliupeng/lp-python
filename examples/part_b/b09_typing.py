"""3.12 上注解会求值；引号形式的前向引用留给 get_type_hints。"""

from typing import get_type_hints


def double(number: int) -> int:
    return number * 2


class Node:
    def __init__(self, nxt: "Node | None" = None) -> None:
        self.nxt = nxt


type IntList = list[int]


def main() -> None:
    assert double.__annotations__["number"] is int
    assert double.__annotations__["return"] is int
    assert double("ab") == "abab"  # 注解不负责拒绝
    assert Node.__init__.__annotations__["nxt"] == "Node | None"
    hints = get_type_hints(Node.__init__)
    assert hints["nxt"] == Node | None
    assert IntList.__value__ == list[int]
    print("ok b09")


if __name__ == "__main__":
    main()
