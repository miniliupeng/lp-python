"""专题 03: 小整数对象池、字符串驻留与同一性判定边界

验证 CPython 小整数池的 [-5, 256] 物理边界、动态驻留机制，
以及严格演示同一性 is 与等价性 == 的本质差异。
"""

import sys


def main() -> None:
    print("=== [01-03] 小整数池、字符串驻留与同一性 (is vs ==) ===")

    # 1. 验证小整数池 [-5, 256] 边界
    in_pool_a = 256
    in_pool_b = 256
    print(f"  • 256 在池内同一性 (in_pool_a is in_pool_b): {in_pool_a is in_pool_b}")
    assert in_pool_a is in_pool_b, "256 必须命中全局静态小整数池单例"

    # 动态构造超出池的数值 (规避编译器常量折叠优化)
    out_pool_a = int("1024")
    out_pool_b = int("1024")
    print(
        f"  • 1024 超出池同一性 (out_pool_a is out_pool_b): {out_pool_a is out_pool_b}"
    )
    print(
        f"  • 1024 等价性比较   (out_pool_a == out_pool_b): {out_pool_a == out_pool_b}"
    )
    assert out_pool_a is not out_pool_b, "超出 256 必须分配独立的堆内存对象"
    assert out_pool_a == out_pool_b, "数值等价但物理内存地址不同"

    # 2. 验证字符串驻留 (String Interning)
    s1 = sys.intern("dynamic_string_token")
    s2 = sys.intern("dynamic_string_token")
    print(f"  • sys.intern 强行驻留后同一性: {s1 is s2}")
    assert s1 is s2, "驻留后的字符串物理地址必须统一"

    # 3. 生产红线提醒
    print("⚠️ 生产红线: 业务代码比较数值或业务字符串时，必须无条件使用 '=='！")
    print("✅ 小整数池与驻留机制验证通过。")


if __name__ == "__main__":
    main()
