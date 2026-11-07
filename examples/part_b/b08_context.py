"""手写上下文管理器与 contextmanager。"""

from __future__ import annotations

from contextlib import contextmanager


class Resource:
    def __init__(self) -> None:
        self.closed = False

    def __enter__(self) -> Resource:
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.closed = True
        return False


@contextmanager
def opened():
    state = {"open": True}
    try:
        yield state
    finally:
        state["open"] = False


def main() -> None:
    resource = Resource()
    with resource:
        assert resource.closed is False
    assert resource.closed is True

    try:
        with Resource() as resource:
            raise RuntimeError("boom")
    except RuntimeError:
        assert resource.closed is True
    else:
        raise AssertionError("异常应继续传播")

    with opened() as state:
        assert state["open"] is True
    assert state["open"] is False
    print("ok b08")


if __name__ == "__main__":
    main()
