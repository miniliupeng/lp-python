"""contextvars 传递请求号；关闭函数只改状态，不发送信号。"""

from __future__ import annotations

import contextvars
import logging
from io import StringIO

REQUEST_ID: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="-"
)


class RequestFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = REQUEST_ID.get()
        return True


class Service:
    def __init__(self) -> None:
        self.running = True

    def handle_sigterm(self) -> None:
        self.running = False


def main() -> None:
    stream = StringIO()
    logger = logging.getLogger("tutorial.d09")
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(request_id)s %(message)s"))
    handler.addFilter(RequestFilter())
    logger.addHandler(handler)

    token = REQUEST_ID.set("r1")
    try:
        logger.info("start")
    finally:
        REQUEST_ID.reset(token)
    logger.info("after")
    assert stream.getvalue().splitlines() == ["r1 start", "- after"]

    service = Service()
    service.handle_sigterm()
    assert service.running is False
    print("ok d09")


if __name__ == "__main__":
    main()
