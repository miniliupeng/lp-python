"""代码对象上能直接看到的执行信息。"""

from __future__ import annotations

import sys


def add(left: int, right: int) -> int:
    return left + right


def main() -> None:
    code = add.__code__
    assert code.co_name == "add"
    assert code.co_varnames[:2] == ("left", "right")
    assert code.co_nlocals >= 2
    assert isinstance(code.co_code, bytes) and code.co_code
    frame = sys._getframe()
    assert frame.f_code.co_name == "main"
    print("ok c01")


if __name__ == "__main__":
    main()
