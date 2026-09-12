"""专题 04: 企业级带参装饰器工厂与 functools.wraps 元数据工程

实现一个生产级通用重试与耗时测量装饰器 retry_and_trace，
保留原函数类型签名与反射元数据，并演示叠放装饰器的执行流转。
"""

import functools
import time
from collections.abc import Callable
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def retry_and_trace(max_attempts: int = 3) -> Callable[[F], F]:
    """工业级带参装饰器工厂: 提供异常自动重试与执行耗时打点."""

    def decorator(func: F) -> F:
        @functools.wraps(func)  # 关键: 完整保留被装饰函数的名称、docstring与签名
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.perf_counter()
            attempts = 0

            while attempts < max_attempts:
                try:
                    attempts += 1
                    result = func(*args, **kwargs)
                    elapsed_ms = (time.perf_counter() - start_time) * 1000
                    print(
                        f"  [Trace] {func.__name__} 执行成功 (耗时: {elapsed_ms:.2f}ms)"
                    )
                    return result
                except Exception as exc:
                    if attempts >= max_attempts:
                        print(f"  [Alert] {func.__name__} 超限 ({max_attempts}次) 抛错")
                        raise
                    print(f"  [Retry] {func.__name__} 重试 {attempts}: {exc}")

        return wrapper  # type: ignore[return-value]

    return decorator


# 模拟业务调用
attempt_counter = 0


@retry_and_trace(max_attempts=3)
def unstable_network_call(target_url: str) -> str:
    """模拟偶发网络抖动并具备自愈能力的下游远程调用接口."""
    global attempt_counter
    attempt_counter += 1
    if attempt_counter < 2:
        raise ConnectionResetError("连接偶发被重置")
    return f"200 OK: {target_url}"


def main() -> None:
    print("=== [03-04] 企业级带参装饰器与元数据保留实战 ===")

    # 1. 验证元数据保留完整性
    print(f"  • 函数真实名称: {unstable_network_call.__name__}")
    print(f"  • 函数文档说明: {unstable_network_call.__doc__}")
    assert unstable_network_call.__name__ == "unstable_network_call", (
        "wraps 必须保留原函数名"
    )

    # 2. 触发重试与链路跟踪
    response = unstable_network_call("https://api.gateway.internal/orders")
    print(f"  • 最终调用产出: {response}")

    print("✅ 带参装饰器工程与反射元数据保护验证完毕。")


if __name__ == "__main__":
    main()
