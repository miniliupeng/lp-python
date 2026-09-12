"""
运算符语义、对象同一性与短路求值机制演示。
展示：is vs ==、短路求值操作数返回、海象运算符 (:=)。
"""

from typing import Any


def demonstrate_identity_vs_equality() -> None:
    """演示同一性 (is) 与等价性 (==) 的严格区别。"""
    list_a: list[int] = [1, 2, 3]
    list_b: list[int] = [1, 2, 3]

    addr_diff = f"{id(list_a)} != {id(list_b)}"
    print(f"[is vs ==] list_a is list_b: {list_a is list_b} (地址不同: {addr_diff})")

    sentinel: Any = None
    print(f"[None Check] sentinel is None 判定: {sentinel is None}")


def demonstrate_short_circuit_logic() -> None:
    """演示 and / or 运算符的短路与值返回特性。"""
    # or 返回第一个真值，全部为假则返回最后一个操作数
    cfg_timeout = 0
    default_timeout = 30
    # 错误用法演示：0 会被当作假值覆盖
    bad_val = cfg_timeout or default_timeout
    # 正确生产规范：基于 None 判断
    safe_val = cfg_timeout if cfg_timeout is not None else default_timeout
    print(f"[Short-circuit Trap] bad: {bad_val}, safe: {safe_val}")

    # and 返回第一个假值，全真则返回最后一个操作数
    res = "DatabaseReady" and {"status": 200}
    print(f"[and Operation] 返回最终决策操作数: {res}")


def demonstrate_walrus_operator() -> None:
    """演示 PEP 572 海象运算符 (:=) 赋值表达式。"""
    data = "production_query_log_payload"
    if (length := len(data)) > 10:
        print(f"[Walrus :=] 匹配长载荷，计算长度: {length}")


def main() -> None:
    print("=== 02. 运算符语义与短路求值 ===")
    demonstrate_identity_vs_equality()
    demonstrate_short_circuit_logic()
    demonstrate_walrus_operator()
    print("=== 演示完成 ===")


if __name__ == "__main__":
    main()
