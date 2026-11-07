"""题库 E03：GIL 切换间隔、取消的基类、队列满。"""

from __future__ import annotations

import asyncio
import queue
import sys


def main() -> None:
    assert sys.getswitchinterval() == 0.005
    assert issubclass(asyncio.CancelledError, BaseException)
    assert not issubclass(asyncio.CancelledError, Exception)
    jobs: queue.Queue[int] = queue.Queue(maxsize=1)
    jobs.put_nowait(1)
    try:
        jobs.put_nowait(2)
    except queue.Full:
        pass
    else:
        raise AssertionError("有界队列会拒绝超额任务")
    print("ok e03")


if __name__ == "__main__":
    main()
