"""短链编码、令牌桶和 LRU。时钟由调用方传入。"""

from __future__ import annotations

from collections import OrderedDict

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"


def encode(number: int) -> str:
    if number < 0:
        raise ValueError("编号不能是负数")
    if number == 0:
        return ALPHABET[0]
    chars: list[str] = []
    base = len(ALPHABET)
    while number:
        number, remainder = divmod(number, base)
        chars.append(ALPHABET[remainder])
    return "".join(reversed(chars))


def decode(text: str) -> int:
    number = 0
    for char in text:
        number = number * len(ALPHABET) + ALPHABET.index(char)
    return number


class TokenBucket:
    def __init__(self, rate: float, capacity: float, now: float) -> None:
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.updated = now

    def allow(self, now: float, cost: float = 1.0) -> bool:
        elapsed = now - self.updated
        self.updated = now
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        if self.tokens < cost:
            return False
        self.tokens -= cost
        return True


class LRU:
    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("容量至少为 1")
        self.capacity = capacity
        self.data: OrderedDict[str, str] = OrderedDict()

    def get(self, key: str) -> str | None:
        if key not in self.data:
            return None
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key: str, value: str) -> None:
        if key in self.data:
            self.data.move_to_end(key)
        self.data[key] = value
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)


def main() -> None:
    assert decode(encode(0)) == 0
    assert decode(encode(36)) == 36
    bucket = TokenBucket(rate=1, capacity=2, now=0)
    assert bucket.allow(0) is True
    assert bucket.allow(0) is True
    assert bucket.allow(0) is False
    assert bucket.allow(1) is True
    cache = LRU(2)
    cache.put("a", "1")
    cache.put("b", "2")
    assert cache.get("a") == "1"
    cache.put("c", "3")
    assert cache.get("b") is None
    assert cache.get("a") == "1"
    print("ok d10")


if __name__ == "__main__":
    main()
