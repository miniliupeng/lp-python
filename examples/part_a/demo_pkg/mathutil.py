"""把数值夹到闭区间里。"""

from __future__ import annotations


def clip(value: int, low: int, high: int) -> int:
    if low > high:
        raise ValueError("low 不能大于 high")
    return max(low, min(high, value))
