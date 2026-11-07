"""浅拷贝、深拷贝，以及不要用 is 比较数值。"""

from __future__ import annotations

import copy
import sys


def main() -> None:
    nested = [[1]]
    shallow = copy.copy(nested)
    shallow[0].append(2)
    assert nested == [[1, 2]]
    assert shallow is not nested

    deep = copy.deepcopy(nested)
    deep[0].append(3)
    assert nested == [[1, 2]]
    assert deep == [[1, 2, 3]]

    cycle: list[object] = []
    cycle.append(cycle)
    cloned = copy.deepcopy(cycle)
    assert cloned[0] is cloned

    built = "".join(["hello", " world"])
    literal = "hello world"
    assert built == literal
    assert built is not literal
    interned = sys.intern(built)
    assert sys.intern(literal) is interned

    assert int("256") is int("256")
    assert int("257") is not int("257")
    print("ok c02")


if __name__ == "__main__":
    main()
