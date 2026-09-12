"""专题 04: 引用计数、循环引用解密与 weakref 弱引用实践

演示引用计数的实时变动、循环引用导致引用计数失效的现场，
触发分代垃圾回收，并使用 weakref 彻底杜绝内存泄漏。
"""

import gc
import sys
import weakref


class Node:
    """定义包含关联引用的节点类."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.peer: object = None


def main() -> None:
    print("=== [01-04] CPython 垃圾回收与 weakref 弱引用实践 ===")
    gc.disable()  # 临时关闭自动 GC 以便观测引用计数真实死锁

    # 1. 制造循环引用孤岛
    node_a = Node("A")
    node_b = Node("B")
    node_a.peer = node_b
    node_b.peer = node_a

    # 删除外部局部强引用
    del node_a
    del node_b
    # 此时两个节点在内存中互指，引用计数均为 1，无法自毁

    # 2. 触发分代垃圾回收 (强制搜寻并清理孤岛)
    unreachable_count = gc.collect()
    print(f"  • gc.collect() 成功识别并回收的不可达孤岛对象数: {unreachable_count}")
    assert unreachable_count > 0, "GC 必须成功检测出循环引用孤岛"

    # 3. 使用 weakref 弱引用彻底从源头避免循环引用
    parent = Node("Parent")
    child = Node("Child")
    # 子节点对父节点建立弱引用 (不增加父节点引用计数)
    child.peer = weakref.ref(parent)

    print(f"  • 父节点当前外部引用计数: {sys.getrefcount(parent) - 1}")
    del parent  # 销毁父节点，父节点引用归零立即析构
    print(f"  • 父节点销毁后，子节点弱引用自动失效返回: {child.peer()}")
    assert child.peer() is None, "目标对象析构后弱引用必须安全回退为 None"

    gc.enable()  # 恢复全局 GC
    print("✅ 循环引用与 weakref 破环方案验证完毕。")


if __name__ == "__main__":
    main()
