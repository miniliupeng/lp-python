"""按当前解释器版本探测 3.13–3.15 才出现的模块，不使用新语法。"""

from __future__ import annotations

import importlib.util
import sys


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def main() -> None:
    version = sys.version_info
    assert version >= (3, 12)
    builtins = sys.modules["builtins"]
    if version < (3, 15):
        assert not hasattr(builtins, "frozendict")
    else:
        assert hasattr(builtins, "frozendict")
    if version < (3, 13):
        assert not hasattr(sys, "_is_gil_enabled")
    else:
        assert sys._is_gil_enabled() in (True, False)
    if version < (3, 14):
        assert not has_module("annotationlib")
        assert not has_module("concurrent.interpreters")
    else:
        assert has_module("annotationlib")
        assert has_module("concurrent.interpreters")
    if version < (3, 15):
        assert not has_module("profiling")
    print(f"ok c07 {version.major}.{version.minor}.{version.micro}")


if __name__ == "__main__":
    main()
