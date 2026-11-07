"""异常层次、raise from，以及 finally 里的 return。"""

from __future__ import annotations


class DomainError(Exception):
    """业务输入不合法。"""


def parse(text: str) -> int:
    try:
        return int(text)
    except ValueError as exc:
        raise DomainError(text) from exc


def finally_wins() -> int:
    try:
        return 1
    finally:
        return 2  # noqa: B012


def main() -> None:
    assert parse("4") == 4
    try:
        parse("no")
    except DomainError as exc:
        assert isinstance(exc.__cause__, ValueError)
    else:
        raise AssertionError("应该抛出 DomainError")
    assert finally_wins() == 2
    try:
        raise KeyboardInterrupt
    except BaseException as exc:
        assert type(exc) is KeyboardInterrupt
        assert not isinstance(exc, Exception)
    print("ok a10")


if __name__ == "__main__":
    main()
