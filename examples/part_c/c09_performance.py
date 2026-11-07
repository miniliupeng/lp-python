"""cProfile 与 tracemalloc 能跑通；不把某次计时当成规则。"""

from __future__ import annotations

import cProfile
import io
import pstats
import tracemalloc
from collections import deque


def by_join(parts: list[str]) -> str:
    return "".join(parts)


def by_plus(parts: list[str]) -> str:
    acc = ""
    for part in parts:
        acc += part
    return acc


def main() -> None:
    parts = ["a"] * 30
    assert by_join(parts) == by_plus(parts)

    profiler = cProfile.Profile()
    profiler.enable()
    by_join(parts)
    profiler.disable()
    buffer = io.StringIO()
    pstats.Stats(profiler, stream=buffer).print_stats()
    assert "by_join" in buffer.getvalue()

    tracemalloc.start()
    held = [0] * 1000
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert peak >= 0
    assert len(held) == 1000

    line: deque[int] = deque()
    line.appendleft(1)
    assert line.popleft() == 1
    print("ok c09")


if __name__ == "__main__":
    main()
