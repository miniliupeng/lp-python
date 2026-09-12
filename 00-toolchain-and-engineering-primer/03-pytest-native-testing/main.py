"""专题 03: 核心业务计算与健壮性验证模块 (待测目标)

本模块包含纯粹自洽的核心数学计算与安全除法业务逻辑，
专供当前专题的单元测试套件进行覆盖率与边界测试。
"""


class CalculationError(Exception):
    """自定义业务计算异常基类."""


def safe_divide(numerator: float, denominator: float) -> float:
    """执行高可用安全除法运算.

    :raises CalculationError: 当除数为 0 或入参不合法时抛出明确业务异常
    """
    if denominator == 0:
        raise CalculationError("除数不能为零 (ZeroDivisionError 业务阻断)")
    return numerator / denominator


def calculate_discount(price: float, discount_rate: float) -> float:
    """计算折后金额并保留两位精度."""
    if not (0.0 <= discount_rate <= 1.0):
        raise ValueError("折扣率必须严格介于 0.0 与 1.0 之间")
    return round(price * discount_rate, 2)


def main() -> None:
    print("=== [00-03] 核心业务计算逻辑运行演示 ===")
    res = safe_divide(100.0, 4.0)
    discounted = calculate_discount(199.9, 0.8)
    print(f"  • 100.0 / 4.0 = {res}")
    print(f"  • 199.9 打 8 折 = {discounted}")
    print("💡 请运行 pytest 执行当前模块专属的测试套件！")


if __name__ == "__main__":
    main()
