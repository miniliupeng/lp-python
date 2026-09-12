"""专题 03: 现代 ASGI 生命周期 (lifespan)、洋葱中间件与全局异常防护

实现标准 lifespan 上下文管理、洋葱耗时拦截中间件，
以及拦截基类 Exception 防护敏感堆栈泄露的生产级全局异常处理器。
"""

import asyncio
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from httpx import ASGITransport, AsyncClient


# 1. 现代标准 ASGI 启停生命周期 (lifespan)
@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("  [Lifespan] 🚀 服务启动期: 预热数据库连接池与全局缓存...")
    yield
    print("  [Lifespan] 🛑 服务优雅停机: 正在安全释放外部长连接...")


app = FastAPI(title="Resilient Enterprise API", lifespan=app_lifespan)


# 2. 洋葱模型中间件: 注入全局 TraceId 与耗时打点
@app.middleware("http")
async def add_process_time_and_audit(request: Request, call_next):  # type: ignore[no-untyped-def]
    start_time = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.2f}"
    return response


# 3. 生产级全局未捕获异常处理器 (防止敏感信息泄露)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    print(f"  [Alert] 生产全局异常兜底拦截: {exc}")
    return JSONResponse(
        status_code=500,
        content={"code": 500, "message": "内部服务遇到未知错误，请联系系统管理员"},
    )


@app.get("/api/v1/trigger-bug")
async def trigger_bug() -> dict[str, str]:
    """故意触发未捕获除零异常的测试接口."""
    _ = 1 / 0
    return {"status": "unreachable"}


async def main() -> None:
    print("=== [07-03] FastAPI 现代生命周期 (lifespan) 与中间件实操 ===")

    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # 请求故意抛错的接口，验证全局异常处理器是否接管返回安全 JSON
        resp = await client.get("/api/v1/trigger-bug")
        print(f"  • 异常拦截响应状态码: {resp.status_code}")
        print(f"  • 中间件注入耗时响应头: {resp.headers.get('x-process-time-ms')}ms")
        print(f"  • 脱敏格式化安全响应:   {resp.json()}")

        assert resp.status_code == 500
        assert resp.json()["code"] == 500
        assert "x-process-time-ms" in resp.headers

    print("✅ lifespan 生命周期、洋葱耗时中间件与全局兜底防御验证通过。")


if __name__ == "__main__":
    asyncio.run(main())
