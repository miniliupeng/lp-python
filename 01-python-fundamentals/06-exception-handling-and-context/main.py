"""
异常分层治理、EAFP 哲学与上下文管理器协议。
展示：try-except-else-finally 完整生命周期、异常链传递、__enter__/__exit__ 协议。
"""

from types import TracebackType


class InfrastructureError(Exception):
    """领域基础设施根异常。"""


class DatabaseConnectionManager:
    """企业级资源上下文管理器，保证连接无论异常与否均能确定性释放。"""

    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self.is_connected = False

    def __enter__(self) -> "DatabaseConnectionManager":
        self.is_connected = True
        print(f"[Context Manager] 已建立连接池资源: {self.dsn}")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        self.is_connected = False
        print(
            f"[Context Manager] 资源确定性回收完毕 (is_connected={self.is_connected})"
        )
        if exc_val:
            exc_name = exc_type.__name__ if exc_type else "None"
            print(f"[Context Manager] 检测到未处理异常冒泡: {exc_name}")
        return False  # 返回 False 允许异常正常向上冒泡传播


def execute_transaction_flow(payload: dict[str, int]) -> str:
    """演示 try-except-else-finally 语义。"""
    try:
        val = payload["amount"]
        result = 1000 // val
    except ZeroDivisionError as err:
        raise InfrastructureError("计算分母不能为零，事务中止") from err
    except KeyError as err:
        raise InfrastructureError(f"缺少必选事务字段: {err}") from err
    else:
        return f"事务计算完成，均分值: {result}"
    finally:
        print("[Finally Guard] 事务链路埋点审计记录完成")


def main() -> None:
    print("=== 06. 异常分层体系与上下文管理器 ===")
    # 正常流与上下文管理
    with DatabaseConnectionManager(
        "postgres://app:secret@db.internal:5432/core"
    ) as conn:
        res = execute_transaction_flow({"amount": 10})
        print(f"执行成功结果: {res} (连接健康: {conn.is_connected})")

    # 异常链测试
    try:
        execute_transaction_flow({"amount": 0})
    except InfrastructureError as e:
        print(
            f"[Chained Exception Caught] 业务异常捕获: {e}, 根因: {repr(e.__cause__)}"
        )

    print("=== 演示完成 ===")


if __name__ == "__main__":
    main()
