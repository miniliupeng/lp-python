"""专题 02: 可变性陷阱、深浅拷贝隔离与默认参数哨兵模式

本示例演示浅拷贝与深拷贝在嵌套结构中的内存指针差异，
并直观展示默认可变参数引发的全局污染及生产级 None 哨兵解决方案。
"""

import copy


def buggy_collector(item: str, bucket: list[str] = []) -> list[str]:  # noqa: B006
    """危险的默认参数写法: bucket 在模块加载时被初始化且全局唯一."""
    bucket.append(item)
    return bucket


def safe_collector(item: str, bucket: list[str] | None = None) -> list[str]:
    """生产级推荐规范: 采用 None 作为不可变哨兵防御全局污染."""
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


def main() -> None:
    print("=== [01-02] 可变性陷阱、深浅拷贝与默认参数安全实践 ===")

    # 1. 深度剖析浅拷贝 vs 深拷贝
    original = {"id": 101, "tags": ["python", "backend"]}
    shallow = copy.copy(original)
    deep = copy.deepcopy(original)

    # 篡改内层可变对象
    shallow["tags"].append("hacked")
    print(f"  • 修改浅拷贝后，原始对象被联动篡改: {original['tags']}")
    print(f"  • 深拷贝内层完全隔离不受影响:       {deep['tags']}")
    assert "hacked" in original["tags"], "浅拷贝嵌套对象共享同一物理引用"
    assert "hacked" not in deep["tags"], "深拷贝完全物理隔离"

    # 2. 验证默认参数全局污染
    _ = buggy_collector("req-A")
    res2 = buggy_collector("req-B")
    print(f"  • 危险调用累加污染结果: {res2} (长度为 {len(res2)})")

    # 3. 验证生产级哨兵安全隔离
    s1 = safe_collector("req-A")
    s2 = safe_collector("req-B")
    print(f"  • 安全哨兵调用结果 A: {s1}")
    print(f"  • 安全哨兵调用结果 B: {s2}")
    assert len(s2) == 1, "None 哨兵确保每次调用生成独立局部容器"
    print("✅ 可变性与深浅拷贝陷阱验证完毕，已掌握生产安全模式。")


if __name__ == "__main__":
    main()
