"""
01-python-fundamentals 单元测试集。
验证：基础数据类型、运算符短路、函数签名、核心容器与异常上下文。
"""

from decimal import Decimal

import pytest


def test_float_vs_decimal() -> None:
    """验证浮点二进制误差与 Decimal 绝对精度。"""
    assert 0.1 + 0.2 != 0.3
    assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3")


def test_short_circuit_operands() -> None:
    """验证 and / or 运算符返回操作数本身。"""
    # or 返回首个真值
    assert (0 or 42) == 42
    assert ("" or "fallback") == "fallback"
    # and 假值短路
    assert (0 and "never") == 0
    assert ("ready" and {"code": 200}) == {"code": 200}


def test_function_signatures_and_sentinel() -> None:
    """验证函数可变参数默认值陷阱与哨兵机制。"""

    def append_item(val: int, container: list[int] | None = None) -> list[int]:
        if container is None:
            container = []
        container.append(val)
        return container

    res1 = append_item(10)
    res2 = append_item(20)
    assert res1 == [10]
    assert res2 == [20]
    assert res1 is not res2


def test_containers_and_generator_memory() -> None:
    """验证字典合并符与生成器表达式惰性求值。"""
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 99, "c": 3}
    merged = d1 | d2
    assert merged == {"a": 1, "b": 99, "c": 3}

    gen = (x * 2 for x in range(3))
    assert next(gen) == 0
    assert next(gen) == 2
    assert next(gen) == 4
    with pytest.raises(StopIteration):
        next(gen)
