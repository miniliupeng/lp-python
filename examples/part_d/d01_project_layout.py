"""教程树只有正文、示例和根说明；项目声明用一段 TOML 演示。"""

from __future__ import annotations

import tomllib
from pathlib import Path

SAMPLE = """
[project]
name = "python-tutorial"
requires-python = ">=3.12"
dependencies = []
"""


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    assert (root / "README.md").is_file()
    assert (root / "docs" / "python-tutorial" / "README.md").is_file()
    assert (root / "examples" / "run_all.py").is_file()
    project = tomllib.loads(SAMPLE)["project"]
    assert project["name"] == "python-tutorial"
    assert project["requires-python"] == ">=3.12"
    assert project["dependencies"] == []
    print("ok d01")


if __name__ == "__main__":
    main()
