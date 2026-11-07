"""按路径顺序运行 examples 下的全部教学脚本。"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def scripts(root: Path) -> list[Path]:
    found: list[Path] = []
    for path in sorted(root.rglob("*.py")):
        if path.name == "run_all.py":
            continue
        if "__pycache__" in path.parts or "demo_pkg" in path.parts:
            continue
        if "cycle_demo" in path.parts:
            continue
        found.append(path)
    return found


def main() -> None:
    root = Path(__file__).resolve().parent
    failed: list[Path] = []
    selected = scripts(root)
    if not selected:
        print("没有找到示例", file=sys.stderr)
        sys.exit(1)
    for path in selected:
        rel = path.relative_to(root)
        print(f"==> {rel}", flush=True)
        result = subprocess.run(
            [sys.executable, str(path)],
            cwd=path.parent,
            check=False,
        )
        if result.returncode != 0:
            failed.append(rel)
    if failed:
        print("失败:", file=sys.stderr)
        for rel in failed:
            print(f"  {rel}", file=sys.stderr)
        sys.exit(1)
    print(f"通过 {len(selected)} 个示例")


if __name__ == "__main__":
    main()
