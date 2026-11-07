"""循环导入的另一侧。"""

from __future__ import annotations

from cycle_demo import left


def marker() -> str:
    return "R"


def via_left() -> str:
    return left.label()
