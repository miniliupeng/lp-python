"""题库 E01 里几条可以用断言钉住的语言事实。"""

from __future__ import annotations


def finally_returns() -> int:
    try:
        return 1
    finally:
        return 2  # noqa: B012


def shared_default(item: int, bucket: list[int] = []) -> list[int]:  # noqa: B006
    bucket.append(item)
    return bucket


def main() -> None:
    assert ("" or "fallback") == "fallback"
    assert -7 // 2 == -4 and -7 % 2 == 1
    assert True + True == 2
    assert (None is None) and not isinstance(None, int)
    nan = float("nan")
    assert nan != nan
    items = [1]
    alias = items
    items += [2]
    assert alias is items
    assert finally_returns() == 2
    assert shared_default(1) == [1]
    assert shared_default(2) == [1, 2]
    try:
        _ = "1" + 1  # type: ignore[operator]
    except TypeError:
        pass
    else:
        raise AssertionError("强类型不会把 str 和 int 相加")
    print("ok e01")


if __name__ == "__main__":
    main()
