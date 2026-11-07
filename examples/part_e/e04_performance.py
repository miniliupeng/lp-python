"""题库 E04：join 与循环拼接结果相同；deque 两端可弹出。"""

from __future__ import annotations

from collections import deque


def main() -> None:
    parts = ["py", "thon"]
    acc = ""
    for part in parts:
        acc += part
    assert acc == "".join(parts)
    line: deque[int] = deque([1, 2, 3])
    line.appendleft(0)
    assert line.pop() == 3
    assert line.popleft() == 0
    assert [0] * 2 == [0, 0]
    grid = [[0] * 1 for _ in range(2)]
    grid[0][0] = 1
    assert grid == [[1], [0]]
    print("ok e04")


if __name__ == "__main__":
    main()
