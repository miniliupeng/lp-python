"""特殊方法：相等、哈希、长度与加法。"""

from __future__ import annotations


class Vec:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: object) -> Vec:
        if not isinstance(other, Vec):
            return NotImplemented
        return Vec(self.x + other.x, self.y + other.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __len__(self) -> int:
        return 2


def main() -> None:
    assert Vec(1, 2) + Vec(3, 4) == Vec(4, 6)
    assert len(Vec(1, 2)) == 2
    assert {Vec(1, 2): "ok"}[Vec(1, 2)] == "ok"
    try:
        Vec(1, 2) + "no"  # type: ignore[operator]
    except TypeError:
        pass
    else:
        raise AssertionError("不相关的类型应返回 NotImplemented 并最终 TypeError")
    print("ok b06")


if __name__ == "__main__":
    main()
