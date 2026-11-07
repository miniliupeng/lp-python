"""把 C 部几条容易说错的结论放在同一组断言里。"""

from __future__ import annotations

import asyncio
import copy
import sys


def main() -> None:
    assert int("256") is int("256")
    assert int("257") is not int("257")
    shared = [[0]]
    alias = copy.copy(shared)
    alias[0][0] = 1
    assert shared[0][0] == 1
    assert sys.getswitchinterval() > 0
    assert not issubclass(asyncio.CancelledError, Exception)
    assert issubclass(bool, int)
    order = {"b": 1}
    order["a"] = 2
    assert list(order) == ["b", "a"]
    print("ok c10")


if __name__ == "__main__":
    main()
