"""TaskGroup、timeout，以及 CancelledError 不继承 Exception。"""

from __future__ import annotations

import asyncio


async def add_later(left: int, right: int) -> int:
    await asyncio.sleep(0)
    return left + right


async def coordinated() -> None:
    async with asyncio.TaskGroup() as group:
        first = group.create_task(add_later(1, 2))
        second = group.create_task(add_later(3, 4))
    assert first.result() == 3
    assert second.result() == 7
    async with asyncio.timeout(1):
        await asyncio.sleep(0)


async def cancelled() -> None:
    async def sleeper() -> None:
        await asyncio.sleep(10)

    task = asyncio.create_task(sleeper())
    await asyncio.sleep(0)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    else:
        raise AssertionError("取消应表现为 CancelledError")
    assert task.cancelled()


def blocking() -> int:
    return 7


async def offload() -> None:
    assert await asyncio.to_thread(blocking) == 7


def main() -> None:
    assert issubclass(asyncio.CancelledError, BaseException)
    assert not issubclass(asyncio.CancelledError, Exception)
    asyncio.run(coordinated())
    asyncio.run(cancelled())
    asyncio.run(offload())
    print("ok c06")


if __name__ == "__main__":
    main()
