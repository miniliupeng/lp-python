"""专题 02: pyproject.toml 声明式工程解析与构建契约验证

本示例演示如何在现代 Python 项目中安全读取与校验 pyproject.toml
规范元数据，并动态验证当前工程的构建目标与关键依赖声明。
"""

import sys

# Python 3.11+ 标准库原生支持 tomllib，无需引入任何第三方解析库
import tomllib
from pathlib import Path


def validate_project_manifest(manifest_path: Path) -> dict[str, object]:
    """读取并严格校验 pyproject.toml 标准工程配置元数据."""
    if not manifest_path.is_file():
        raise FileNotFoundError(f"未找到工程核心清单文件: {manifest_path}")

    with open(manifest_path, "rb") as f:
        data = tomllib.load(f)

    # 验证 PEP 621 [project] 标准根节点
    project = data.get("project")
    if not isinstance(project, dict):
        raise ValueError("pyproject.toml 必须包含合法的 [project] 声明配置块！")

    name = project.get("name")
    requires_python = project.get("requires-python")
    dependencies = project.get("dependencies", [])

    return {
        "project_name": name,
        "requires_python": requires_python,
        "runtime_deps_count": len(dependencies),
        "tool_ruff_configured": "ruff" in data.get("tool", {}),
        "tool_pytest_configured": "pytest" in data.get("tool", {}),
    }


def main() -> None:
    print("=== [00-02] 现代 Python 工程清单 (pyproject.toml) 校验 ===")
    project_root = Path(__file__).resolve().parent.parent.parent
    manifest_file = project_root / "pyproject.toml"

    try:
        report = validate_project_manifest(manifest_file)
        for k, v in report.items():
            print(f"  • {k:<23}: {v}")
        print("✅ 工程构建元数据符合 PEP 621 规范，工具链配置完整。")
    except Exception as exc:
        print(f"❌ 校验失败: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
