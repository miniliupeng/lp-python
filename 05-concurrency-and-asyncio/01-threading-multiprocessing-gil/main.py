"""专题 01: GIL 表现特征、多线程与多进程算力实测对比

演示 CPU 密集型计算在多线程与多进程模式下的真实耗时差异，
并直观验证多进程如何打破 GIL 束缚利用多核。
"""

import concurrent.futures
import time


def cpu_intensive_task(n: int) -> int:
    """CPU 密集型斐波那契累加计算."""
    count = 0
    for i in range(n):
        count += i * i
    return count


def main() -> None:
    print("=== [04-01] GIL 表现分析: 多线程 vs 多进程算力对比 ===")
    task_size = 5_000_000
    task_runs = 2

    # 1. 多线程模式执行 CPU 密集任务 (受 GIL 串行锁制约)
    start_threads = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(cpu_intensive_task, task_size) for _ in range(task_runs)
        ]
        concurrent.futures.wait(futures)
    time_threads = time.perf_counter() - start_threads
    print(f"  • 多线程执行 2 个计算任务耗时: {time_threads:.3f} 秒 (受限于 GIL 互斥)")

    # 2. 多进程模式执行 CPU 密集任务 (突破 GIL 真正多核并行)
    start_processes = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(cpu_intensive_task, task_size) for _ in range(task_runs)
        ]
        concurrent.futures.wait(futures)
    time_processes = time.perf_counter() - start_processes
    print(
        f"  • 多进程执行 2 个计算任务耗时: {time_processes:.3f} 秒 (突破 GIL 多核并行)"
    )

    print(f"  • 多进程加速比: {(time_threads / max(time_processes, 0.001)):.2f}x")
    print("✅ GIL 影响验证完成: CPU 密集计算首选多进程，I/O 并发首选 asyncio。")


if __name__ == "__main__":
    main()
