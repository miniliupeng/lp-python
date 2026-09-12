"""专题 03: FastAPI 原生 SSE 流式打字机与流式管道实操."""

import asyncio
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from httpx import ASGITransport, AsyncClient

app = FastAPI(title="AI Streaming Gateway")


async def fake_llm_token_generator(prompt: str) -> AsyncGenerator[str, None]:
    """模拟大模型异步流式吐出 Token 序列."""
    tokens = ["根据", "您的", "提问", "，现代", "Python", "架构", "已全面", "就绪。"]
    for token in tokens:
        await asyncio.sleep(0.005)
        yield "data: " + token + "\n\n"
    yield "data: [DONE]\n\n"


@app.get("/api/v1/chat/stream")
async def chat_streaming_endpoint(prompt: str = "hello") -> StreamingResponse:
    """生产级标准 SSE 流式响应端点."""
    return StreamingResponse(
        fake_llm_token_generator(prompt),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


async def main() -> None:
    print("=== [08-03] FastAPI 原生 SSE 流式打字机实操 ===")

    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        collected: list[str] = []
        async with client.stream("GET", "/api/v1/chat/stream") as response:
            assert response.headers["content-type"].startswith("text/event-stream")
            print("  • 逐帧接收 Token: ", end="", flush=True)

            async for chunk in response.aiter_text():
                for line in chunk.splitlines():
                    if line.startswith("data: ") and line != "data: [DONE]":
                        word = line.replace("data: ", "")
                        print(word, end="", flush=True)
                        collected.append(word)

        print("\n  • [Stream] [DONE] 帧到达，流式传输安全关闭")
        assert len(collected) > 0, "必须成功逐帧消费到流式 Token"

    print("✅ FastAPI 原生 SSE 流式打字机管道验证通过。")


if __name__ == "__main__":
    asyncio.run(main())
