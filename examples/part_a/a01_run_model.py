"""脚本入口、表达式和函数对象。"""

from __future__ import annotations


def add(left: int, right: int) -> int:
    return left + right


def main() -> None:
    assert add(2, 3) == 5
    assert __name__ == "__main__"
    bound = add
    assert bound(10, 1) == 11
    label = "py"
    assert f"{label=}" == "label='py'"
    print("ok a01")


if __name__ == "__main__":
    main()
