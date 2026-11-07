"""导入包，并演示安全的循环导入形态。"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cycle_demo.left import label  # noqa: E402
from cycle_demo.right import via_left  # noqa: E402
from demo_pkg import clip  # noqa: E402


def main() -> None:
    assert clip(10, 0, 3) == 3
    assert clip(-1, 0, 3) == 0
    assert label() == "LR"
    assert via_left() == "LR"
    print("ok a11")


if __name__ == "__main__":
    main()
