"""专题 02: FastAPI Depends 依赖注入系统、子依赖树与 yield 资源管理

演示通过 Depends 实现身份鉴权、请求级数据库会话依赖，
以及利用 yield 语法实现请求完毕后的自动化资源提交与安全清理。
"""

import asyncio
from collections.abc import AsyncGenerator

from fastapi import Depends, FastAPI, Header, HTTPException
from httpx import ASGITransport, AsyncClient

app = FastAPI(title="Dependency Injection Architecture")


async def get_db_session() -> AsyncGenerator[dict[str, str], None]:
    """模拟数据库请求级会话: 利用 yield 实现自动化生命周期治理."""
    session = {"session_id": "sess-8899", "status": "active"}
    print(f"  [Dependency] 数据库会话 {session['session_id']} 建立，已开启事务")
    try:
        yield session  # 注入下游使用
        print(f"  [Dependency] 业务成功执行，会话 {session['session_id']} 自动 Commit")
    finally:
        session["status"] = "closed"
        print(f"  [Dependency] 会话 {session['session_id']} 已安全 Close 归还连接池")


async def get_authenticated_user(
    x_token: str = Header(..., description="用户访问凭证"),
    db: dict[str, str] = Depends(get_db_session),
) -> dict[str, str]:
    """嵌套子依赖: 校验 Token 合法性，并复用同一个数据库会话."""
    if x_token != "secret-token-123":
        raise HTTPException(status_code=401, detail="非法访问凭证")
    return {"user_id": "usr-101", "role": "admin", "session": db["session_id"]}


@app.get("/api/v1/profile")
async def read_profile(
    user: dict[str, str] = Depends(get_authenticated_user),
) -> dict[str, str]:
    """受保护的业务核心端点."""
    return {"message": "success", "user": user["user_id"], "role": user["role"]}


async def main() -> None:
    print("=== [07-02] FastAPI Depends 依赖注入与生命周期实操 ===")

    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # 1. 模拟未带有效 Token 的非法请求
        unauth_resp = await client.get("/api/v1/profile")
        print(f"  • 未授权请求拦截响应码: {unauth_resp.status_code}")
        assert unauth_resp.status_code == 422  # 缺少必须请求头

        # 2. 模拟携带有效凭证的合法请求 (观察控制台依赖与 yield 清理时序)
        headers = {"x-token": "secret-token-123"}
        resp = await client.get("/api/v1/profile", headers=headers)
        print(f"  • 授权业务请求响应体:   {resp.json()}")

        assert resp.status_code == 200
        assert resp.json()["user"] == "usr-101"

    print("✅ Depends 依赖树注入与 yield 资源确定性析构验证全部通过。")


if __name__ == "__main__":
    asyncio.run(main())
