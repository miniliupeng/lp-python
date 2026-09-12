"""专题 03: pytest 现代化单元测试套件

涵盖参数化数据驱动测试、异常抛出逆向断言以及 Fixture 上下文生命周期管理。
"""

import pytest
from main import CalculationError, calculate_discount, safe_divide


@pytest.fixture
def mock_pricing_context() -> dict[str, float]:
    """提供测试上下文数据源的 Fixture 示例."""
    ctx = {"base_price": 200.0, "vip_discount": 0.85}
    yield ctx
    ctx.clear()


def test_safe_divide_success() -> None:
    """验证安全除法正向正常计算."""
    result = safe_divide(10.0, 2.0)
    assert result == 5.0, "两数相除计算结果应符合数学预期"


def test_safe_divide_zero_division_raises() -> None:
    """验证除以零时正确抛出业务自定义异常."""
    with pytest.raises(CalculationError, match="除数不能为零"):
        safe_divide(10.0, 0.0)


@pytest.mark.parametrize(
    ("price", "rate", "expected"),
    [
        (100.0, 0.9, 90.0),
        (50.0, 0.5, 25.0),
        (199.99, 1.0, 199.99),
        (88.0, 0.0, 0.0),
    ],
)
def test_calculate_discount_parametrized(
    price: float, rate: float, expected: float
) -> None:
    """使用参数化矩阵高效测试多组折扣计算边界."""
    assert calculate_discount(price, rate) == expected


def test_fixture_injection(mock_pricing_context: dict[str, float]) -> None:
    """验证 Fixture 依赖注入机制."""
    price = mock_pricing_context["base_price"]
    rate = mock_pricing_context["vip_discount"]
    assert calculate_discount(price, rate) == 170.0
