"""循环导入的一侧。"""

from __future__ import annotations

from cycle_demo import right


def label() -> str:
    return "L" + right.marker()
