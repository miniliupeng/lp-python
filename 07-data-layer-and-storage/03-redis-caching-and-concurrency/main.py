"""专题 03: 异步 Redis 客户端、防穿透/击穿/雪崩与分布式锁实战."""

import asyncio
import random


class MockAsyncRedis:
    """模拟异步 Redis 客户端 (自洽无真实网络强依赖运行)."""

    def __init__(self) -> None:
        self.store: dict[str, str] = {}

    async def get(self, key: str) -> str | None:
        await asyncio.sleep(0.001)
        return self.store.get(key)

    async def set(self, key: str, val: str, nx: bool = False, ex: int = 60) -> bool:
        await asyncio.sleep(0.001)
        if nx and key in self.store:
            return False
        self.store[key] = val
        return True

    async def delete(self, key: str) -> None:
        self.store.pop(key, None)


async def get_with_cache_defense(user_id: str, redis: MockAsyncRedis) -> str:
    """具备三剑客完整防御的工业级缓存读取模式."""
    cache_key = f"user:profile:{user_id}"
    cached = await redis.get(cache_key)
    if cached is not None:
        return cached

    # 1. 缓存未命中: 抢占原子互斥锁防击穿 (SET NX)
    lock_key = f"lock:{cache_key}"
    if not await redis.set(lock_key, "locked", nx=True, ex=5):
        await asyncio.sleep(0.01)
        return await redis.get(cache_key) or "FallbackData"

    try:
        # 2. 回源查询数据
        db_data = None if user_id == "illegal-999" else f"Data[{user_id}]"

        # 3. 防穿透(空值缓存) + 防雪崩(TTL随机抖动)
        if db_data is None:
            await redis.set(cache_key, "NULL_SENTINEL", ex=60)
            return "NULL_SENTINEL"

        jitter = random.randint(10, 60)
        await redis.set(cache_key, db_data, ex=3600 + jitter)
        return db_data
    finally:
        await redis.delete(lock_key)


async def main() -> None:
    print("=== [06-03] 异步 Redis 缓存治理与分布式锁防护实操 ===")
    redis = MockAsyncRedis()

    # 验证防穿透
    res_null = await get_with_cache_defense("illegal-999", redis)
    print(f"  • 防穿透回源空值安全缓存: {res_null}")
    assert res_null == "NULL_SENTINEL"

    # 验证防击穿高并发锁
    tasks = [get_with_cache_defense("vip-1001", redis) for _ in range(3)]
    results = await asyncio.gather(*tasks)
    print(f"  • 并发防击穿回源结果: {results}")
    assert all(r == "Data[vip-1001]" for r in results)
    print("✅ 缓存穿透/击穿/雪崩防御与原子锁验证通过。")


if __name__ == "__main__":
    asyncio.run(main())
