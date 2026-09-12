"""专题 04: 生成器状态机、惰性流式处理与 send() 双向通信

演示生成器相比列表推导式的 O(1) 内存优势，并通过 send()
实现一个生产级动态可调节移动平均值（Moving Average）计算协程。
"""

import sys
from collections.abc import Generator


def fibonacci_stream(limit: int) -> Generator[int, None, None]:
    """生成斐波那契惰性数据流 (O(1) 内存占用)."""
    a, b = 0, 1
    for _ in range(limit):
        yield a
        a, b = b, a + b


def moving_average_coroutine() -> Generator[float, float, None]:
    """基于 yield 表达式与 send() 实现的双向通信累加平均值协程."""
    total = 0.0
    count = 0
    current_avg = 0.0

    while True:
        # yield 返回当前均值，并挂起等待外部通过 send(val) 注入新数据
        new_val = yield current_avg
        total += new_val
        count += 1
        current_avg = total / count


def main() -> None:
    print("=== [02-04] 生成器状态机与 send() 双向通信实战 ===")

    # 1. 验证生成器对象的极低内存占用
    fib_gen = fibonacci_stream(10000)
    print(f"  • 斐波那契生成器对象大小: {sys.getsizeof(fib_gen)} 字节 (恒定常数大小)")

    # 提取前 5 项
    first_five = [next(fib_gen) for _ in range(5)]
    print(f"  • 惰性计算前 5 项结果:    {first_five}")
    assert first_five == [0, 1, 1, 2, 3], "生成器计算结果符合预期"

    # 2. 验证 send() 双向通信协程
    avg_calc = moving_average_coroutine()
    # 协程必须预激 (调用一次 next 推进至第一个 yield 处挂起)
    next(avg_calc)

    avg1 = avg_calc.send(10.0)
    avg2 = avg_calc.send(20.0)
    avg3 = avg_calc.send(30.0)
    print(f"  • 注入 10.0 后的移动均值: {avg1}")
    print(f"  • 注入 20.0 后的移动均值: {avg2}")
    print(f"  • 注入 30.0 后的移动均值: {avg3}")
    assert avg3 == 20.0, "累加均值计算必须精确"

    avg_calc.close()  # 安全关闭协程
    print("✅ 生成器惰性状态机与双向通信验证完毕。")


if __name__ == "__main__":
    main()
