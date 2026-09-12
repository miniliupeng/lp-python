"""专题 01: FastAPI 异步高性能内核、APIRouter 路由与内存测试实战

构建自洽的 FastAPI 异步服务，结合 Pydantic 契约与 APIRouter，
并通过 httpx.ASGITransport 在内存中进行免端口占用的快速测试验证。
"""

import asyncio

from fastapi import APIRouter, FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import BaseModel, Field

# 1. 构建主应用与路由契约
app = FastAPI(title="Modern Enterprise API")
order_router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


class CreateOrderRequest(BaseModel):
    item_id: str = Field(min_length=3)
    quantity: int = Field(ge=1, le=100)


class OrderResponse(BaseModel):
    order_id: str
    status: str


@order_router.post("", response_model=OrderResponse, status_code=201)
async def create_order(payload: CreateOrderRequest) -> OrderResponse:
    """异步创建订单处理路由."""
    # 模拟非阻塞微服务调用
    await asyncio.sleep(0.005)
    return OrderResponse(order_id=f"ord-{payload.item_id}-99", status="created")


app.include_router(order_router)


async def main() -> None:
    print("=== [07-01] FastAPI 异步内核、路由与声明式契约实操 ===")

    # 2. 使用 httpx ASGITransport 在内存测试 ASGI 实例
    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # 正向请求验证
        payload = {"item_id": "laptop-pro", "quantity": 2}
        resp = await client.post("/api/v1/orders", json=payload)
        print(f"  • 创建订单响应码: {resp.status_code}")
        print(f"  • 创建订单响应体: {resp.json()}")

        assert resp.status_code == 201
        assert resp.json()["order_id"] == "ord-laptop-pro-99"

        # 逆向非法入参校验 (验证 Pydantic 自动拦截 422 Unprocessable Entity)
        bad_resp = await client.post(
            "/api/v1/orders", json={"item_id": "x", "quantity": 0}
        )
        print(f"  • 非法入参触发自动防御响应码: {bad_resp.status_code}")
        assert bad_resp.status_code == 422

    print("✅ FastAPI 异步路由与内存测试链路验证全部通过。")


if __name__ == "__main__":
    asyncio.run(main())
