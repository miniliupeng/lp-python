"""专题 02: 现代函数签名契约 (/ 与 *) 及闭包延迟绑定规避

演示位置专用参数、关键字专用参数的强契约约束，
并直观展示闭包延迟绑定的严重 Bug 及基于默认参数的立即绑定解法。
"""

from collections.abc import Callable


def modern_api_service(
    endpoint: str,
    /,  # 位置专用: 外部严禁用 endpoint="xxx" 调用，便于内部解耦重命名
    retry_count: int = 3,
    *,  # 关键字专用: 之后的所有参数调用方必须显式写明名称
    enable_ssl: bool = True,
    timeout: float = 5.0,
) -> str:
    """现代企业级强契约函数签名定义."""
    return (
        f"Service[{endpoint}] retry={retry_count} ssl={enable_ssl} timeout={timeout}s"
    )


def demonstrate_closure_late_binding() -> None:
    """演示闭包延迟绑定的经典陷阱与标准解决方案."""
    # ❌ 错误做法: 延迟绑定陷阱
    bad_handlers: list[Callable[[], int]] = []
    for i in range(3):
        bad_handlers.append(lambda: i)  # noqa: B023  # i 在调用时才求值，最终都读到 2

    bad_results = [h() for h in bad_handlers]
    print(f"  • 延迟绑定陷阱输出 (全部错变为最后值): {bad_results}")
    assert bad_results == [2, 2, 2], "未即时绑定的闭包全部共享最终循环状态"

    # ✅ 正确解法: 利用默认参数在定义期立即求值冻结快照
    good_handlers: list[Callable[[], int]] = []
    for i in range(3):
        good_handlers.append(lambda captured_i=i: captured_i)

    good_results = [h() for h in good_handlers]
    print(f"  • 默认参数即时求值快照输出:             {good_results}")
    assert good_results == [0, 1, 2], "默认参数在循环遍历瞬间完成值捕获"


def main() -> None:
    print("=== [02-02] 函数签名规范 (/ 与 *) 与闭包作用域实战 ===")

    # 1. 验证强签名契约
    res = modern_api_service(
        "https://api.internal/v1", 2, enable_ssl=True, timeout=10.0
    )
    print(f"  • 契约函数调用成功: {res}")

    # 2. 闭包延迟绑定实验
    demonstrate_closure_late_binding()
    print("✅ 现代函数签名与闭包延迟绑定治理方案验证通过。")


if __name__ == "__main__":
    main()
