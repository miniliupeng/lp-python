"""结构模式匹配。字符串单独处理，避免被当成二元序列。"""

from __future__ import annotations


def describe(value: object) -> str:
    match value:
        case str():
            return "text"
        case (x, y) if x == y:
            return "same-pair"
        case (_, _):
            return "pair"
        case {"ok": True, "n": int(n)}:
            return f"ok-{n}"
        case [0, *rest]:
            return f"lead0-{len(rest)}"
        case _:
            return "other"


def main() -> None:
    assert describe("no") == "text"
    assert describe((1, 1)) == "same-pair"
    assert describe((1, 2)) == "pair"
    assert describe({"ok": True, "n": 4, "extra": 1}) == "ok-4"
    assert describe([0, 8, 9]) == "lead0-2"
    assert describe(3) == "other"
    print("ok b10")


if __name__ == "__main__":
    main()
