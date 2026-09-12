"""
核心内置容器性能模型、推导式与惰性生成器对比。
展示：list/dict/set 高效操作、推导式 vs 生成器内存对比、deque 队列。
"""

import sys
from collections import deque


def demonstrate_container_ops() -> None:
    """演示现代字典合并与双向队列的高效增删。"""
    base_config = {"host": "localhost", "port": 8000}
    env_config = {"port": 9000, "debug": True}
    # Python 3.9+ 字典合并运算符 (|)
    merged = base_config | env_config
    print(f"[Dict Merge] 覆盖后配置: {merged}")

    # 高性能队列：首尾增删 O(1)
    queue: deque[str] = deque(maxlen=3)
    queue.append("task-1")
    queue.append("task-2")
    queue.append("task-3")
    queue.append("task-4")  # 触发溢出自动挤出 task-1
    print(f"[Deque FIFO] 溢出自动剔除: {list(queue)}")


def demonstrate_comprehension_vs_generator() -> None:
    """演示列表推导式 (即时求值) 与生成器表达式 (惰性求值) 的内存消耗。"""
    # 列表推导式：立即分配全部内存
    list_comp = [i * 2 for i in range(1000)]
    # 生成器表达式：仅保存迭代状态指针
    gen_expr = (i * 2 for i in range(1000))

    mem_l = sys.getsizeof(list_comp)
    mem_g = sys.getsizeof(gen_expr)
    print(f"[Memory Contrast] 列表推导式: {mem_l} 字节, 生成器: {mem_g} 字节 (O(1))")


def main() -> None:
    print("=== 05. 核心容器体系与推导式 ===")
    demonstrate_container_ops()
    demonstrate_comprehension_vs_generator()
    print("=== 演示完成 ===")


if __name__ == "__main__":
    main()
