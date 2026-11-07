"""确认本仓库用 pyproject.toml 声明 3.12，且示例不改这个文件。"""

from __future__ import annotations

import tomllib
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    project_file = root / "pyproject.toml"
    data = tomllib.loads(project_file.read_text(encoding="utf-8"))
    project = data["project"]
    assert project["name"] == "lp-python"
    assert project["requires-python"] == ">=3.12"
    assert (root / "docs" / "python-tutorial" / "README.md").is_file()
    assert (root / "00-toolchain-and-engineering-primer").is_dir()
    print("ok d01")


if __name__ == "__main__":
    main()
