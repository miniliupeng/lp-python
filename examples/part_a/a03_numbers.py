"""整数、浮点、Decimal、bool 与 None。"""

from __future__ import annotations

from decimal import Decimal


def returns_257() -> int:
    return 257


def main() -> None:
    assert 7 / 2 == 3.5
    assert 7 // 2 == 3
    assert -7 // 2 == -4
    assert -7 % 2 == 1
    assert divmod(-7, 2) == (-4, 1)
    assert 0.1 + 0.2 != 0.3
    assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3")
    assert True + True == 2
    assert False == 0
    assert (None is None) and (None == None)  # noqa: E711
    nan = float("nan")
    assert nan != nan
    assert int("256") is int("256")
    assert int("257") is not int("257")
    assert returns_257() is returns_257()
    print("ok a03")


if __name__ == "__main__":
    main()
