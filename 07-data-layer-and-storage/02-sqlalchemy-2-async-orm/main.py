"""专题 02: SQLAlchemy 2.0 现代异步 ORM、声明式实体与事务生命周期

使用 SQLAlchemy 2.0 + aiosqlite 构建纯异步持久层，
实现基于 Mapped 强类型声明式模型、显式 select 语法与原子事务提交。
"""

import asyncio

from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """SQLAlchemy 2.0 统一强类型声明式基类."""


class UserAccount(Base):
    """用户持久化账户实体模型."""

    __tablename__ = "user_accounts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    tier: Mapped[str] = mapped_column(String(20), default="standard")


async def main() -> None:
    print("=== [06-02] SQLAlchemy 2.0 异步 ORM 与事务管理实操 ===")

    # 1. 创建异步引擎 (基于内存 SQLite)
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    # 自动生成数据库 Schema 架构
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("  • 成功基于 Mapped 声明式模型完成数据库表架构构建")

    # 2. 在安全上下文会话中执行插入与提交
    async with async_session() as session:
        user = UserAccount(username="architect_max", tier="vip")
        session.add(user)
        await session.commit()
        print(f"  • 用户入库成功: id={user.id}, tier={user.tier}")

    # 3. 使用标准 2.0 select 语法进行强契约检索
    async with async_session() as session:
        stmt = select(UserAccount).where(UserAccount.username == "architect_max")
        result = await session.execute(stmt)
        record = result.scalar_one_or_none()

        assert record is not None, "必须精确检索到已插入的数据"
        print(f"  • 2.0 select 检索结果: 用户={record.username}, 等级={record.tier}")

    await engine.dispose()  # 安全释放连接池
    print("✅ SQLAlchemy 2.0 异步引擎、事务控制与连接池验证通过。")


if __name__ == "__main__":
    asyncio.run(main())
