"""pathlib 与显式文本编码。"""

from __future__ import annotations

import tempfile
from pathlib import Path


def main() -> None:
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        path = root / "notes" / "hello.txt"
        path.parent.mkdir()
        path.write_text("你好\n第二行\n", encoding="utf-8")
        assert path.read_text(encoding="utf-8").splitlines() == ["你好", "第二行"]
        assert path.suffix == ".txt"
        assert path.relative_to(root) == Path("notes") / "hello.txt"
        names = sorted(p.name for p in path.parent.iterdir())
        assert names == ["hello.txt"]
    print("ok a09")


if __name__ == "__main__":
    main()
