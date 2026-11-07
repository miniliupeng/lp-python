"""引用计数立即回收，循环引用交给 gc。"""

from __future__ import annotations

import gc
import weakref


class Node:
    def __init__(self) -> None:
        self.other: Node | None = None


def main() -> None:
    box = Node()
    ref = weakref.ref(box)
    del box
    assert ref() is None

    try:
        weakref.ref([])
    except TypeError:
        pass
    else:
        raise AssertionError("list 不能创建弱引用")

    gone: list[str] = []
    left = Node()
    right = Node()
    left.other = right
    right.other = left
    # 弱引用对象本身必须留着，回调才会在目标被回收时触发。
    held = [
        weakref.ref(left, lambda _ref: gone.append("L")),
        weakref.ref(right, lambda _ref: gone.append("R")),
    ]
    del left, right
    gc.collect()
    assert set(gone) == {"L", "R"}
    assert all(item() is None for item in held)
    print("ok c03")


if __name__ == "__main__":
    main()
