"""锁保护共享计数；进程池在独立解释器里计算。"""

from __future__ import annotations

import sys
import threading
from concurrent.futures import ProcessPoolExecutor


def square(number: int) -> int:
    return number * number


def bump(lock: threading.Lock, counter: list[int], times: int) -> None:
    for _ in range(times):
        with lock:
            counter[0] += 1


def main() -> None:
    assert sys.getswitchinterval() == 0.005
    counter = [0]
    lock = threading.Lock()
    threads = [
        threading.Thread(target=bump, args=(lock, counter, 1000)) for _ in range(4)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert counter[0] == 4000

    with ProcessPoolExecutor(max_workers=2) as pool:
        assert list(pool.map(square, [1, 2, 3])) == [1, 4, 9]
    print("ok c05")


if __name__ == "__main__":
    main()
