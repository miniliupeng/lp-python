"""库存流水：枚举表示方向，不够扣时拒绝。"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Side(Enum):
    IN = "in"
    OUT = "out"


@dataclass(frozen=True)
class Movement:
    sku: str
    qty: int
    side: Side

    def __post_init__(self) -> None:
        if self.qty <= 0:
            raise ValueError("数量必须是正数")


@dataclass
class Stock:
    on_hand: dict[str, int] = field(default_factory=dict)

    def apply(self, move: Movement) -> None:
        current = self.on_hand.get(move.sku, 0)
        delta = move.qty if move.side is Side.IN else -move.qty
        nxt = current + delta
        if nxt < 0:
            raise ValueError("库存不能为负")
        self.on_hand[move.sku] = nxt


def main() -> None:
    stock = Stock()
    stock.apply(Movement("pen", 5, Side.IN))
    stock.apply(Movement("pen", 2, Side.OUT))
    assert stock.on_hand["pen"] == 3
    try:
        stock.apply(Movement("pen", 4, Side.OUT))
    except ValueError:
        pass
    else:
        raise AssertionError("超卖应被拒绝")
    assert stock.on_hand["pen"] == 3
    try:
        Movement("pen", 0, Side.IN)
    except ValueError:
        pass
    else:
        raise AssertionError("非正数量应被拒绝")
    print("ok b13")


if __name__ == "__main__":
    main()
