"""yield、yield from、send 与 close。"""

from __future__ import annotations


def countdown(start: int):
    while start > 0:
        received = yield start
        if received is not None:
            start = received
            continue
        start -= 1


def chain():
    yield from (1, 2)
    yield from (3,)


def main() -> None:
    gen = countdown(2)
    assert next(gen) == 2
    assert gen.send(5) == 5
    assert next(gen) == 4
    gen.close()
    try:
        next(gen)
    except StopIteration:
        pass
    else:
        raise AssertionError("close 之后不能继续")
    assert list(chain()) == [1, 2, 3]
    print("ok b03")


if __name__ == "__main__":
    main()
