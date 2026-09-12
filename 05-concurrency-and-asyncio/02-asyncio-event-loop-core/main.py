"""专题 02: asyncio 单线程事件循环核心调度与 Task 并发流转

演示协程对象的惰性本质、Task 对象的立即调度机制，
以及对比串行 await 与 asyncio.create_task 并发推进的执行时序。
"""

import asyncio
import time


async def mock_async_network_io(request_id: str, delay_sec: float) -> str:
    """模拟非阻塞异步网络 I/O 请求."""
    # 必须使用 asyncio.sleep 而非 time.sleep 以出让 CPU 控制权
    await asyncio.sleep(delay_sec)
    return f"Response[{request_id}]"


async def main() -> None:
    print("=== [04-02] asyncio 单线程事件循环与 Task 调度实操 ===")

    # 1. 验证单一协程的惰性创建
    coro = mock_async_network_io("req-0", 0.01)
    print(f"  • 协程对象类型: {type(coro).__name__} (尚未启动)")

    # 2. 串行 await (耗时累加)
    t0 = time.perf_counter()
    _ = await mock_async_network_io("serial-1", 0.05)
    _ = await mock_async_network_io("serial-2", 0.05)
    serial_elapsed = time.perf_counter() - t0
    print(f"  • 串行执行 2 个任务耗时: {serial_elapsed:.3f}s (耗时累加)")

    # 3. 通过 create_task 实现单线程高并发交替调度 (耗时取最大值)
    t1 = time.perf_counter()
    task1 = asyncio.create_task(mock_async_network_io("task-1", 0.05))
    task2 = asyncio.create_task(mock_async_network_io("task-2", 0.05))

    # 并发等待两个已在事件循环中运行的 Task 完成
    results = await asyncio.gather(task1, task2)
    concurrent_elapsed = time.perf_counter() - t1
    print(f"  • Task 并发调度 2 个任务耗时: {concurrent_elapsed:.3f}s (耗时重叠)")
    print(f"  • 并发执行结果快照: {results}")

    assert concurrent_elapsed < (serial_elapsed * 0.7), "并发执行必须大幅快于串行累加"
    print("✅ asyncio 单线程事件循环与 Task 异步并发机制验证通过。")


if __name__ == "__main__":
    asyncio.run(main())
