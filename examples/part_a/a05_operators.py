"""比较、短路、增强赋值和解包。"""

from __future__ import annotations


def main() -> None:
    assert 1 < 2 < 3
    assert ("" or "fallback") == "fallback"
    assert (0 and 1) == 0
    assert (1 and "ok") == "ok"
    items = [1]
    alias = items
    items += [2]
    assert alias is items and alias == [1, 2]
    pair = (1,)
    other = pair
    pair += (2,)
    assert pair == (1, 2) and pair is not other
    assert (n := 4) * n == 16
    assert {1: "a"} | {1: "b", 2: "c"} == {1: "b", 2: "c"}
    first, *rest = [10, 20, 30]
    assert first == 10 and rest == [20, 30]
    print("ok a05")


if __name__ == "__main__":
    main()
