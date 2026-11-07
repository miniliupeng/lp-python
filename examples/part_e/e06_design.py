"""题库 E06：容量有限的缓存会丢掉最久未使用的键。"""

from __future__ import annotations

from collections import OrderedDict


class LRU:
    def __init__(self, capacity: int) -> None:
        self.data: OrderedDict[str, int] = OrderedDict()
        self.capacity = capacity

    def get(self, key: str) -> int | None:
        if key not in self.data:
            return None
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key: str, value: int) -> None:
        if key in self.data:
            self.data.move_to_end(key)
        self.data[key] = value
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)


def main() -> None:
    cache = LRU(1)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") is None
    assert cache.get("b") == 2
    print("ok e06")


if __name__ == "__main__":
    main()
