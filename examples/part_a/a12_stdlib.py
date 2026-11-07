"""入门阶段会反复用到的一小部分标准库。"""

from __future__ import annotations

import json
import math
import random
import statistics
from datetime import UTC, datetime


def main() -> None:
    payload = json.loads('{"n": 2}')
    assert payload["n"] == 2
    assert json.dumps({"n": 2}, sort_keys=True) == '{"n": 2}'
    moment = datetime(2026, 11, 7, tzinfo=UTC)
    assert moment.year == 2026
    assert math.isclose(math.sqrt(4), 2.0)
    rng = random.Random(0)
    again = random.Random(0)
    left = [rng.randrange(5) for _ in range(3)]
    right = [again.randrange(5) for _ in range(3)]
    assert left == right
    assert statistics.mean([1, 2, 3]) == 2
    print("ok a12")


if __name__ == "__main__":
    main()
