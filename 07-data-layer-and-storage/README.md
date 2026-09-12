# 阶段 07: 存储层、持久化与异步 ORM

数据持久化与缓存是后端业务的命脉。本阶段覆盖现代异步驱动体系下的原生 SQLite 预编译防注入、SQLAlchemy 2.0 异步 Session 生命周期，以及 Redis 分布式缓存防穿透、击穿与雪崩的工业级治理实践。

---

## 💡 核心工程心智与底层机制

1. **异步驱动与参数化预编译防注入**：
   - 坚决杜绝在 SQL 字符串中进行拼接或使用格式化字符串；
   - 掌握通过 `aiosqlite` 异步执行预编译占位符参数绑定（Prepared Statements），从协议层物理杜绝 SQL 注入攻击。
2. **SQLAlchemy 2.0 异步生态与 Session 生命周期**：
   - 彻底摆脱 1.x 时代的同步阻塞与隐式懒加载（Implicit Lazy Loading）雷区；
   - 拥抱 `async_sessionmaker` 与 `select()` 声明式 2.0 语法；采用异步上下文管理器（`async with`）严防生产连接池耗尽与泄漏。
3. **Redis 异步缓存与高并发三大痛点治理**：
   - 缓存穿透（Cache Penetration）：空值缓存与布隆过滤器拦截；
   - 缓存击穿（Cache Breakdown）：热点 Key 过期前夕通过分布式互斥锁（Mutex Lock）拦截并发打穿；
   - 缓存雪崩（Cache Avalanche）：批量 Key 过期时间加入随机扰动偏置（Jitter），防止瞬间压垮底层数据库。

---

## 🗺️ 阶段专题导航

| 专题目录 | 核心原语 | 关键掌握目标 |
| :--- | :--- | :--- |
| **[01-sqlite-async-prepared-statements](./01-sqlite-async-prepared-statements/)** | 异步嵌入式数据库与参数化查询 | 掌握 aiosqlite 异步执行、游标游历与参数化防 SQL 注入 |
| **[02-sqlalchemy-2-async-orm](./02-sqlalchemy-2-async-orm/)** | SQLAlchemy 2.0 异步 Session | 掌握 DeclarativeBase 模型定义、异步事务提交与连接池防泄漏 |
| **[03-redis-caching-and-concurrency](./03-redis-caching-and-concurrency/)** | 异步 Redis 缓存与雪崩治理 | 掌握 redis.asyncio 缓存层、互斥锁与随机 TTL 扰动雪崩防护 SOP |

---

## 🚀 统一运行验证

```bash
uv run python 07-data-layer-and-storage/01-sqlite-async-prepared-statements/main.py
uv run python 07-data-layer-and-storage/02-sqlalchemy-2-async-orm/main.py
uv run python 07-data-layer-and-storage/03-redis-caching-and-concurrency/main.py
```
