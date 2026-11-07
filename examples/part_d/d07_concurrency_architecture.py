"""有界队列拒绝超额放入；消费者读到哨兵后停止。"""

from __future__ import annotations

import queue
import threading

STOP = object()


def consume(jobs: queue.Queue[object], out: list[int]) -> None:
    while True:
        item = jobs.get()
        try:
            if item is STOP:
                return
            if not isinstance(item, int):
                raise TypeError("任务必须是 int")
            out.append(item * 2)
        finally:
            jobs.task_done()


def main() -> None:
    bounded: queue.Queue[int] = queue.Queue(maxsize=1)
    bounded.put(1)
    try:
        bounded.put_nowait(2)
    except queue.Full:
        pass
    else:
        raise AssertionError("满队列应拒绝")
    assert bounded.get() == 1

    jobs: queue.Queue[object] = queue.Queue()
    out: list[int] = []
    worker = threading.Thread(target=consume, args=(jobs, out))
    worker.start()
    for number in (1, 2, 3):
        jobs.put(number)
    jobs.put(STOP)
    worker.join()
    assert out == [2, 4, 6]
    print("ok d07")


if __name__ == "__main__":
    main()
