"""路径约束、常量时间比较，以及不把 pickle 当安全边界。"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import tempfile
from pathlib import Path


def safe_join(root: Path, name: str) -> Path:
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("非法路径")
    candidate = (root / relative).resolve()
    root_resolved = root.resolve()
    if candidate != root_resolved and root_resolved not in candidate.parents:
        raise ValueError("路径逃出根目录")
    return candidate


def sign(key: bytes, message: bytes) -> str:
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def main() -> None:
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        path = safe_join(root, "notes/a.txt")
        assert root.resolve() in path.parents
        try:
            safe_join(root, "../secret")
        except ValueError:
            pass
        else:
            raise AssertionError("父目录片段应被拒绝")

    key = secrets.token_bytes(16)
    mac = sign(key, b"body")
    assert hmac.compare_digest(mac, sign(key, b"body"))
    assert not hmac.compare_digest(mac, sign(key, b"bode"))
    print("ok d08")


if __name__ == "__main__":
    main()
