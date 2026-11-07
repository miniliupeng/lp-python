"""分支、循环，以及循环和 try 上的 else。"""

from __future__ import annotations


def classify(n: int) -> str:
    if n < 0:
        return "neg"
    if n == 0:
        return "zero"
    return "pos"


def loop_else(values: list[int]) -> str:
    for item in values:
        if item < 0:
            break
    else:
        return "all-non-negative"
    return "found-negative"


def try_else(text: str) -> str:
    try:
        int(text)
    except ValueError:
        return "bad"
    else:
        return "good"


def main() -> None:
    assert classify(-1) == "neg" and classify(0) == "zero"
    total = 0
    n = 0
    while n < 3:
        n += 1
        if n == 2:
            continue
        total += n
    assert total == 4
    assert loop_else([1, 2]) == "all-non-negative"
    assert loop_else([1, -1]) == "found-negative"
    assert try_else("3") == "good"
    assert try_else("x") == "bad"
    print("ok a06")


if __name__ == "__main__":
    main()
