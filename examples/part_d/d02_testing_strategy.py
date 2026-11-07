"""把时钟注进去，测试不必睡眠。"""

from __future__ import annotations


class Clock:
    def __init__(self, now: float) -> None:
        self.now = now

    def time(self) -> float:
        return self.now


def is_expired(created_at: float, ttl: float, clock: Clock) -> bool:
    return clock.time() >= created_at + ttl


def main() -> None:
    clock = Clock(100.0)
    assert is_expired(90.0, 5.0, clock) is True
    assert is_expired(99.0, 5.0, clock) is False
    clock.now = 104.0
    assert is_expired(99.0, 5.0, clock) is True
    print("ok d02")


if __name__ == "__main__":
    main()
