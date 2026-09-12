"""专题 01: PyObject 核心结构探针与变量名绑定模型

本示例利用标准库与 ctypes 窥探 CPython 底层 PyObject 结构体，
验证引用计数的变化、类型指针的同一性与名称重新绑定的真实行为。
"""

import ctypes
import sys


class PyObjectHead(ctypes.Structure):
    """映射 CPython 底层 PyObject 基础头部结构 (PyObject_HEAD)."""

    _fields_ = [
        ("ob_refcnt", ctypes.c_ssize_t),
        ("ob_type", ctypes.c_void_p),
    ]


def inspect_pyobject(target: object) -> tuple[int, int]:
    """通过内存物理地址直接读取 PyObject 头部的引用计数与类型指针."""
    address = id(target)
    head = PyObjectHead.from_address(address)
    return head.ob_refcnt, head.ob_type


def main() -> None:
    print("=== [01-01] PyObject 底层内存结构与变量绑定探针 ===")

    # 1. 创建堆对象并检查初始引用
    val = [1, 2, 3]  # 避免小整数常量池干扰
    addr = id(val)
    refcnt, type_ptr = inspect_pyobject(val)
    print(f"  • 对象物理地址: 0x{addr:x}")
    print(f"  • 底层引用计数: {refcnt} (sys.getrefcount 视窗: {sys.getrefcount(val)})")
    print(f"  • 类型指针地址: 0x{type_ptr:x} (对照 id(list): 0x{id(list):x})")

    # 2. 验证多标签绑定 (指针赋值)
    alias = val
    refcnt_after_bind, _ = inspect_pyobject(val)
    print(f"  • alias = val 绑定后引用计数增加为: {refcnt_after_bind}")
    assert alias is val, "alias 与 val 必须指向完全相同的堆内存物理地址"

    # 3. 验证解除绑定
    del alias
    refcnt_after_del, _ = inspect_pyobject(val)
    print(f"  • del alias 解除绑定后引用计数回落至: {refcnt_after_del}")
    print("✅ PyObject 内存模型验证完毕，变量实质为指针引用标签。")


if __name__ == "__main__":
    main()
