"""参数化写入与事务回滚。"""

from __future__ import annotations

import sqlite3


def main() -> None:
    connection = sqlite3.connect(":memory:")
    connection.execute("create table note(id integer primary key, body text not null)")
    try:
        with connection:
            connection.execute("insert into note(body) values (?)", ("a",))
            raise RuntimeError("boom")
    except RuntimeError:
        pass
    count = connection.execute("select count(*) from note").fetchone()
    assert count is not None and count[0] == 0

    payload = "x'; drop table note; --"
    with connection:
        connection.execute("insert into note(body) values (?)", (payload,))
    row = connection.execute("select body from note").fetchone()
    assert row == (payload,)
    still = connection.execute(
        "select count(*) from sqlite_master where type='table' and name='note'"
    ).fetchone()
    assert still is not None and still[0] == 1
    print("ok d06")


if __name__ == "__main__":
    main()
