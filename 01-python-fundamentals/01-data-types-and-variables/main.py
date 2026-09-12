"""
数据类型与动态变量绑定模型演示。
展示：动态引用绑定、IEEE 754 浮点误差 vs Decimal 金融精度、类型标注。
"""

import sys
from decimal import Decimal


def demonstrate_variable_binding() -> None:
    """演示名字绑定机制与不可变对象内存引用。"""
    x: int = 100
    addr_x = id(x)
    x += 1  # 创建新对象并重新绑定引用
    print(f"[Variable Binding] x 从 {addr_x} 变更为新对象地址: {id(x)}")


def demonstrate_float_precision_vs_decimal() -> None:
    """演示 IEEE 754 浮点陷阱与 Decimal 生产选型。"""
    # 浮点数二进制精度丢失
    f_sum: float = 0.1 + 0.2
    print(f"[Float Trap] 0.1 + 0.2 == 0.3 -> {f_sum == 0.3} (实际值: {f_sum:.17f})")

    # 生产级金融计算方案
    d1 = Decimal("0.1")
    d2 = Decimal("0.2")
    d_sum = d1 + d2
    is_equal = d_sum == Decimal("0.3")
    print(f"[Decimal Safe] Decimal 0.1 + 0.2 == 0.3 -> {is_equal}")


def demonstrate_type_introspection() -> None:
    """演示运行时类型内省与系统大小。"""
    val: str = "NexusEngine"
    v_type = type(val).__name__
    v_size = sys.getsizeof(val)
    print(f"[Type Introspection] 类型: {v_type}, 占用: {v_size} 字节")


def main() -> None:
    print("=== 01. 数据类型与动态变量模型 ===")
    demonstrate_variable_binding()
    demonstrate_float_precision_vs_decimal()
    demonstrate_type_introspection()
    print("=== 演示完成 ===")


if __name__ == "__main__":
    main()
