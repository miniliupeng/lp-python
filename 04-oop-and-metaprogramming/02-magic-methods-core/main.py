"""专题 02: 核心魔术方法系统与哈希表检索契约

实现一个具备不可变特性的身份令牌类，协同重载 __repr__、
__eq__、__hash__ 与 __call__，演示哈希表检索的内部时序。
"""


class ImmutableToken:
    """不可变凭证实体: 严格遵守哈希一致性协议 (Hash Contract)."""

    def __init__(self, token_id: str, scope: str) -> None:
        self._token_id = token_id
        self._scope = scope

    @property
    def token_id(self) -> str:
        return self._token_id

    def __repr__(self) -> str:
        """面向调试与日志的明确表达契约."""
        return f"ImmutableToken(token_id={self._token_id!r}, scope={self._scope!r})"

    def __eq__(self, other: object) -> bool:
        """等价性比较: 基于关键业务字段判定."""
        if not isinstance(other, ImmutableToken):
            return False
        return self._token_id == other._token_id and self._scope == other._scope

    def __hash__(self) -> int:
        """哈希一致性计算: 仅对不可变字段计算元组哈希."""
        return hash((self._token_id, self._scope))

    def __call__(self, client_id: str) -> str:
        """让实例像函数一样可直接调用 (Callable 协议)."""
        return f"授权客户端 [{client_id}] 访问权限: {self._scope}"


def main() -> None:
    print("=== [03-02] 核心魔术方法与哈希一致性契约实操 ===")

    t1 = ImmutableToken("tok-1001", "read:orders")
    t2 = ImmutableToken("tok-1001", "read:orders")
    t3 = ImmutableToken("tok-1002", "write:orders")

    # 1. 验证 __repr__ 调试友好度
    print(f"  • 实体 repr 日志快照: {t1!r}")

    # 2. 验证 __eq__ 与 __hash__ 协同
    print(f"  • t1 == t2 值等价性: {t1 == t2}")
    print(f"  • hash(t1) == hash(t2): {hash(t1) == hash(t2)}")
    assert t1 == t2, "等价性判定必须成立"
    assert hash(t1) == hash(t2), "等价对象的哈希值必须无条件相等"

    # 3. 验证哈希集合去重 (Set / Dict Key)
    token_registry = {t1: " active", t3: "revoked"}
    print(f"  • 字典检索命中状态: {token_registry.get(t2)}")
    assert token_registry[t2] == " active", "t2 必须能够精准检索到 t1 存入的哈希键"

    # 4. 验证 __call__ 可调用对象
    auth_result = t1("service-billing")
    print(f"  • __call__ 可调用对象执行结果: {auth_result}")

    print("✅ 魔术方法系统与哈希一致性协议验证全部通过。")


if __name__ == "__main__":
    main()
