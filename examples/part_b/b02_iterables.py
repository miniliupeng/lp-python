"""可迭代对象、迭代器和推导式。"""

from __future__ import annotations


class CountDown:
    def __init__(self, start: int) -> None:
        self.start = start

    def __iter__(self):
        current = self.start
        while current > 0:
            yield current
            current -= 1


def main() -> None:
    data = [10, 20]
    assert list(data) == list(data)
    iterator = iter(data)
    assert next(iterator) == 10
    assert list(iterator) == [20]
    try:
        next(iterator)
    except StopIteration:
        pass
    else:
        raise AssertionError("耗尽的迭代器应停止")

    assert list(CountDown(3)) == [3, 2, 1]
    assert [n * n for n in range(4) if n % 2 == 0] == [0, 4]
    assert {word[0] for word in ["ada", "grace", "lin"]} == {"a", "g", "l"}
    assert {n: n * n for n in range(3)} == {0: 0, 1: 1, 2: 4}
    squares = (n * n for n in range(3))
    assert next(squares) == 0
    assert list(squares) == [1, 4]
    print("ok b02")


if __name__ == "__main__":
    main()
