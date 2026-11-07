"""str、bytes 与编码。"""

from __future__ import annotations


def main() -> None:
    text = "héllo"
    assert len(text) == 5
    assert text[0] == "h"
    raw = text.encode("utf-8")
    assert isinstance(raw, bytes)
    assert raw.decode("utf-8") == text
    assert ",".join(["a", "b", "c"]) == "a,b,c"
    name = "Ada"
    assert f"{name} {1 + 1}" == "Ada 2"
    assert f"{name=}" == "name='Ada'"
    assert r"\n" == "\\n"
    buf = bytearray(b"ab")
    buf[0] = ord("z")
    assert bytes(buf) == b"zb"
    try:
        text[0] = "H"  # type: ignore[index]
    except TypeError:
        pass
    else:
        raise AssertionError("str 不能按索引赋值")
    print("ok a04")


if __name__ == "__main__":
    main()
