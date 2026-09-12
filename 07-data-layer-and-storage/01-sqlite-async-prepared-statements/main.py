"""专题 01: 异步 SQLite 操作、预编译参数化防注入与 WAL 模式实战

使用 aiosqlite 建立异步连接，开启 WAL 读写并发模式，
演示恶意注入载荷在预编译参数化下被严格作为纯字面量安全处理。
"""

import asyncio

import aiosqlite


async def main() -> None:
    print("=== [06-01] 异步 SQLite、预编译防注入与 WAL 模式实操 ===")

    # 1. 建立异步连接并开启 WAL 模式
    async with aiosqlite.connect(":memory:") as db:
        await db.execute("PRAGMA journal_mode=WAL;")
        await db.execute(
            """
            CREATE TABLE accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                balance REAL NOT NULL
            )
            """
        )
        await db.commit()
        print("  • 成功创建 accounts 表，已开启 WAL 读写并发模式")

        # 2. 插入测试种子数据
        await db.execute(
            "INSERT INTO accounts (username, balance) VALUES (?, ?)",
            ("admin_user", 9999.0),
        )
        await db.commit()

        # 3. 模拟黑客构造的恶意 SQL 注入攻击载荷
        hacker_input = "non_existent' OR '1'='1"
        print(f"  • 黑客恶意输入载荷: {hacker_input}")

        # ✅ 使用预编译参数化占位符 (?) 执行安全检索
        safe_sql = "SELECT id, username, balance FROM accounts WHERE username = ?"
        async with db.execute(safe_sql, (hacker_input,)) as cursor:
            rows = await cursor.fetchall()
            print(f"  • 预编译参数化安全查询命中记录数: {len(rows)}")
            assert len(rows) == 0, "预编译必须将输入视为纯字符串，绝不能被注入穿透！"

        # 正常查询验证
        async with db.execute(safe_sql, ("admin_user",)) as cursor:
            admin_row = await cursor.fetchone()
            print(f"  • 正常查询成功召回记录: {admin_row}")
            assert admin_row is not None and admin_row[1] == "admin_user"

    print("✅ 预编译语句防注入机制与异步 SQLite 驱动验证通过。")


if __name__ == "__main__":
    asyncio.run(main())
