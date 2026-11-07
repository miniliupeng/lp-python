"""用 dis 观察指令名，不断言会随版本变化的完整字节码。"""

from __future__ import annotations

import dis


def add(left: int, right: int) -> int:
    return left + right


def main() -> None:
    names = [instruction.opname for instruction in dis.get_instructions(add)]
    assert "LOAD_FAST" in names
    assert "BINARY_OP" in names
    assert "RETURN_VALUE" in names
    assert add.__code__.co_stacksize >= 1
    print("ok c04")


if __name__ == "__main__":
    main()
