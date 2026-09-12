"""专题 04: 异步高并发池控制 (Semaphore) 与背压保护实操

使用 asyncio.Semaphore 构建一个最大并发度为 3 的异步任务调度池，
调度 8 个并发任务，实时监控并验证同一时刻活跃并发数绝不超标。
"""

import asyncio


class ConcurrencyController:
    """基于信号量的生产级异步并发限制池."""

    def __init__(self, max_concurrent: int) -> None:
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.active_count = 0

    async def execute_task(self, task_id: int) -> str:
        """受控执行异步任务并监控实时并发水位."""
        async with self.semaphore:
            self.active_count += 1
            print(f"  [Start] 任务 {task_id:02d} (活跃数: {self.active_count})")
            assert self.active_count <= 3, "活跃并发数绝对严禁超过信号量上限 3！"

            # 模拟耗时网络 I/O 交互
            await asyncio.sleep(0.04)

            self.active_count -= 1
            print(f"  [Done]  任务 {task_id:02d} (剩余活跃: {self.active_count})")
            return f"Result-{task_id}"


async def main() -> None:
    print("=== [04-04] asyncio.Semaphore 高并发限制池与背压实战 ===")
    controller = ConcurrencyController(max_concurrent=3)

    # 派发 8 个并发任务进入受控调度池
    tasks = [controller.execute_task(i) for i in range(1, 9)]
    results = await asyncio.gather(*tasks)

    print(f"  • 全量任务受控执行完毕，结果集数量: {len(results)}")
    assert len(results) == 8, "所有受控任务必须全部平稳执行"
    print("✅ Semaphore 滑动窗口并发控制与防打爆机制验证通过。")


if __name__ == "__main__":
    asyncio.run(main())
