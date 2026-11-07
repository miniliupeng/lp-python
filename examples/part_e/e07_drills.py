"""手写小题：重试、分组、生成器管道。"""

from __future__ import annotations

import functools


def retry(times: int):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last: BaseException | None = None
            for _ in range(times):
                try:
                    return fn(*args, **kwargs)
                except RuntimeError as exc:
                    last = exc
            assert last is not None
            raise last

        return wrapper

    return decorator


def group(rows: list[tuple[str, int]]) -> dict[str, list[int]]:
    grouped: dict[str, list[int]] = {}
    for key, value in rows:
        grouped.setdefault(key, []).append(value)
    return grouped


def pipeline(numbers: list[int]):
    for number in numbers:
        if number % 2 == 0:
            yield number * number


class Flaky:
    def __init__(self) -> None:
        self.calls = 0

    @retry(3)
    def run(self) -> str:
        self.calls += 1
        if self.calls < 3:
            raise RuntimeError("not yet")
        return "ok"


def main() -> None:
    job = Flaky()
    assert job.run() == "ok"
    assert job.calls == 3
    assert group([("a", 1), ("b", 2), ("a", 3)]) == {"a": [1, 3], "b": [2]}
    assert list(pipeline([1, 2, 3, 4])) == [4, 16]
    print("ok e07")


if __name__ == "__main__":
    main()
