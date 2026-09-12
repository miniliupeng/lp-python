"""专题 01: 极速包管理、虚拟环境隔离与 CPython 运行时探针

本示例演示如何通过 Python 标准库探针，精确检测当前进程的运行时环境、
虚拟环境隔离状态、解释器架构与内存寻址能力。
"""

import platform
import sys


def inspect_runtime_environment() -> dict[str, object]:
    """探测当前 Python 进程的运行时元数据与环境隔离边界."""
    # 判断是否运行在虚拟环境的核心逻辑: sys.prefix 与 sys.base_prefix 是否脱钩
    is_virtual_env = sys.prefix != sys.base_prefix

    return {
        "python_version": platform.python_version(),
        "interpreter": platform.python_implementation(),
        "architecture": platform.architecture()[0],
        "is_virtual_env": is_virtual_env,
        "executable_path": sys.executable,
        "virtual_env_path": sys.prefix if is_virtual_env else None,
        "base_system_path": sys.base_prefix,
        "pointer_size_bits": 64 if sys.maxsize > 2**32 else 32,
    }


def main() -> None:
    print("=== [00-01] Python 现代工程运行时与虚拟环境探针 ===")
    info = inspect_runtime_environment()

    for key, val in info.items():
        print(f"  • {key:<18}: {val}")

    # 验证关键环境安全红线
    if not info["is_virtual_env"]:
        print("[警告] 当前进程未在隔离虚拟环境中运行，存在全局环境污染风险！")
    else:
        print("✅ 虚拟环境隔离有效，项目依赖已被严格限定在独立上下文。")


if __name__ == "__main__":
    main()
