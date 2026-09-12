"""专题 01: 现代类型系统与 typing.Protocol 结构化契约实战

演示基于 typing.Protocol 的非侵入式结构化子类型 (鸭子类型静态化)，
解耦业务依赖注入，并利用 @runtime_checkable 实现运行时类型探针。
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class CacheClientProtocol(Protocol):
    """定义缓存客户端结构化契约 (无需外部实现类显式继承)."""

    def get(self, key: str) -> str | None: ...
    def set(self, key: str, value: str, ttl_sec: int = 3600) -> bool: ...


class ThirdPartyRedisAdapter:
    """模拟第三方/未继承协议的纯粹原生类."""

    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        return self._store.get(key)

    def set(self, key: str, value: str, ttl_sec: int = 3600) -> bool:
        self._store[key] = value
        return True


def fetch_user_data(user_id: str, cache: CacheClientProtocol) -> str:
    """业务函数: 仅依赖抽象协议，不绑定任何具体实现类."""
    cached = cache.get(user_id)
    if cached:
        return f"CacheHit[{cached}]"

    fresh_data = f"UserRecord-{user_id}"
    cache.set(user_id, fresh_data)
    return f"DBFetch[{fresh_data}]"


def main() -> None:
    print("=== [05-01] typing.Protocol 结构化鸭子类型契约实操 ===")
    adapter = ThirdPartyRedisAdapter()

    # 1. 验证运行时结构匹配探针
    is_valid_cache = isinstance(adapter, CacheClientProtocol)
    print(f"  • 第三方适配器是否符合 CacheClientProtocol: {is_valid_cache}")
    assert is_valid_cache, "适配器实现了对应方法签名，必须被判定为协议子类型"

    # 2. 执行依赖注入调用
    res1 = fetch_user_data("usr-8899", adapter)
    res2 = fetch_user_data("usr-8899", adapter)
    print(f"  • 首次请求 (穿透回源): {res1}")
    print(f"  • 二次请求 (命中缓存): {res2}")

    assert res2 == "CacheHit[UserRecord-usr-8899]", "协议依赖注入行为符合预期"
    print("✅ Protocol 结构化子类型验证完毕，实现非侵入式依赖解耦。")


if __name__ == "__main__":
    main()
