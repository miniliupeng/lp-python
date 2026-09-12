"""
现代函数签名设计、参数解构协议与可变默认值陷阱防御。
展示：可变默认参数陷阱、位置/关键字专用形参 (/ 与 *)、参数解包。
"""

from typing import Any


def dangerous_append(val: int, target: list[int] = []) -> list[int]:  # noqa: B006
    """反模式：共享静态可变列表。"""
    target.append(val)
    return target


def safe_append(val: int, target: list[int] | None = None) -> list[int]:
    """生产规范：使用 None 哨兵对象实现隔离。"""
    if target is None:
        target = []
    target.append(val)
    return target


def create_endpoint(
    path: str,
    /,  # 之前必须是位置参数
    *,  # 之后必须是关键字专用参数
    timeout_sec: float = 5.0,
    enable_cache: bool = False,
) -> dict[str, Any]:
    """工业级 API 签名设计：强制关键配置必须显式具名调用。"""
    return {
        "path": path,
        "timeout": timeout_sec,
        "cache": enable_cache,
    }


def main() -> None:
    print("=== 04. 函数签名与参数解构 ===")
    # 演示可变参数陷阱
    res1 = dangerous_append(1)
    res2 = dangerous_append(2)
    print(f"[Trap Triggered] 共享内存列表污染: res1={res1}, res2={res2}")

    # 演示哨兵模式修复
    safe1 = safe_append(1)
    safe2 = safe_append(2)
    print(f"[Safe Sentinel] 独立调用隔离: safe1={safe1}, safe2={safe2}")

    # 现代函数签名校验
    endpoint = create_endpoint("/api/v1/users", timeout_sec=2.5, enable_cache=True)
    print(f"[API Signature] 具名安全调用成功: {endpoint}")
    print("=== 演示完成 ===")


if __name__ == "__main__":
    main()
