"""题库 E05：配置来自参数，日志不打印传入的令牌。"""

from __future__ import annotations

import logging
from io import StringIO


def load_port(env: dict[str, str], default: int = 8000) -> int:
    raw = env.get("PORT", str(default))
    port = int(raw)
    if not 1 <= port <= 65535:
        raise ValueError("端口超出范围")
    return port


def main() -> None:
    assert load_port({}) == 8000
    assert load_port({"PORT": "80"}) == 80
    stream = StringIO()
    logger = logging.getLogger("tutorial.e05")
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(stream)
    logger.addHandler(handler)
    token = "secret"
    logger.info("server started")
    assert token not in stream.getvalue()
    print("ok e05")


if __name__ == "__main__":
    main()
