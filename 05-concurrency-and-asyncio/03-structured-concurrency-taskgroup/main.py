"""专题 03: 结构化并发 (TaskGroup) 与 ExceptionGroup 异常树实战

演示 Python 3.11+ TaskGroup 的生命周期边界约束、
单任务失败时对同组兄弟任务的级联取消 (Cancel)，以及 ExceptionGroup 捕获。
"""

import asyncio


async def reliable_worker(task_id: int) -> str:
    """模拟正常运行并感知取消信号的可靠任务."""
    try:
        await asyncio.sleep(0.5)
        return f"Worker[{task_id}] 正常完成"
    except asyncio.CancelledError:
        print(f"  [Cancel] Worker[{task_id}] 感知到同伴异常，已安全响应级联取消信号")
        raise  # 必须重新抛出以完成协程安全退出


async def faulty_worker() -> None:
    """模拟执行发生异常的故障任务."""
    await asyncio.sleep(0.05)
    raise ConnectionResetError("底层网络连接被异常断开")


async def main() -> None:
    print("=== [04-03] 结构化并发 (asyncio.TaskGroup) 实操 ===")

    # 验证 TaskGroup 的异常级联取消与 ExceptionGroup 聚合
    try:
        async with asyncio.TaskGroup() as tg:
            # 派生两个并发任务: 一个快速失败，一个原本耗时较长
            tg.create_task(reliable_worker(1))
            tg.create_task(faulty_worker())
            print("  • TaskGroup 已创建两个协同任务并启动执行...")

    except* ConnectionResetError as eg:  # Python 3.11+ 异常组模式匹配
        print(f"  • 成功捕获并发异常组 (ExceptionGroup): {eg.exceptions}")
        print("  • 验证成功: 故障任务抛错后，同组正常任务已被自动取消，杜绝孤儿泄漏！")

    print("✅ 结构化并发 TaskGroup 作用域与级联取消机制验证通过。")


if __name__ == "__main__":
    asyncio.run(main())
