"""专题 03: 描述符协议 (__get__, __set__) 与 ORM 字段校验实战

手写一个轻量级强类型校验数据描述符 TypedField，
实现字段类型自动校验、__set_name__ 自动属性绑定与实例状态隔离。
"""

from typing import Any


class TypedField:
    """现代数据描述符: 负责拦截属性赋值并强制执行类型安全契约."""

    def __init__(self, expected_type: type) -> None:
        self.expected_type = expected_type
        self.storage_name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        """Python 3.6+: 类创建时由解释器自动回调，注入字段名."""
        self.storage_name = f"_descriptor_{name}"

    def __get__(self, instance: object, owner: type) -> Any:
        if instance is None:
            return self  # 通过类直接访问时返回描述符自身
        return getattr(instance, self.storage_name, None)

    def __set__(self, instance: object, value: Any) -> None:
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"字段 [{self.storage_name}] 类型非法: "
                f"期望 {self.expected_type.__name__}, 实际 {type(value).__name__}"
            )
        # 将数据保存在具体实例内部，彻底隔离各实例状态
        setattr(instance, self.storage_name, value)


class UserProfile:
    """应用描述符的实体模型类 (模拟 ORM/契约模型)."""

    username = TypedField(str)
    age = TypedField(int)

    def __init__(self, username: str, age: int) -> None:
        self.username = username
        self.age = age


def main() -> None:
    print("=== [03-03] 描述符协议与 ORM 强类型拦截实战 ===")

    # 1. 正常构造实体
    u1 = UserProfile("alice", 25)
    u2 = UserProfile("bob", 30)

    print(f"  • u1 用户名: {u1.username}, 年龄: {u1.age}")
    print(f"  • u2 用户名: {u2.username}, 年龄: {u2.age}")
    assert u1.username == "alice" and u2.username == "bob", "多实例状态必须隔离"

    # 2. 触发描述符的类型防御性拦截
    try:
        u1.age = "not_a_number"  # 故意传入非法字符串
        print("❌ 错误: 描述符未能拦截非法类型注入")
    except TypeError as exc:
        print(f"  • 描述符成功拦截非法赋值: {exc}")

    print("✅ 描述符协议与属性读写拦截验证全部通过。")


if __name__ == "__main__":
    main()
