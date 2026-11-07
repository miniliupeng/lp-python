"""日志走 handler；过滤器去掉固定的敏感片段。"""

from __future__ import annotations

import logging
from io import StringIO


class Redact(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = str(record.msg).replace("secret", "***")
        return True


def main() -> None:
    stream = StringIO()
    logger = logging.getLogger("tutorial.d04")
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    handler.addFilter(Redact())
    logger.addHandler(handler)
    logger.info("ready")
    logger.info("token=secret")
    lines = stream.getvalue().splitlines()
    assert lines == ["INFO ready", "INFO token=***"]
    print("ok d04")


if __name__ == "__main__":
    main()
