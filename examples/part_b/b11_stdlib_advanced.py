"""collections、itertools、functools 与正则的常用切片。"""

from __future__ import annotations

import re
from collections import Counter, defaultdict, deque
from functools import cache
from itertools import batched, groupby


@cache
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def main() -> None:
    counts = Counter("aab")
    assert counts["a"] == 2
    assert counts.most_common(1) == [("a", 2)]

    line: deque[int] = deque()
    line.append(1)
    line.appendleft(0)
    assert list(line) == [0, 1]

    grouped: dict[str, list[str]] = defaultdict(list)
    grouped["k"].append("v")
    assert grouped["k"] == ["v"]

    pairs = list(batched([1, 2, 3, 4, 5], 2))
    assert pairs == [(1, 2), (3, 4), (5,)]

    rows = [("a", 1), ("a", 2), ("b", 3)]
    chunks = []
    for key, group in groupby(rows, lambda row: row[0]):
        chunks.append((key, [item for _, item in group]))
    assert chunks == [("a", [1, 2]), ("b", [3])]

    assert fib(8) == 21
    assert re.findall(r"\d+", "a12b3") == ["12", "3"]
    print("ok b11")


if __name__ == "__main__":
    main()
