"""list、tuple、dict、set 的别名、顺序和可哈希约束。"""

from __future__ import annotations


def main() -> None:
    nums = [3, 1, 2]
    nums.append(0)
    assert sorted(nums) == [0, 1, 2, 3]
    assert nums[0] == 3
    aliased = [[0] * 2] * 2
    aliased[0][0] = 1
    assert aliased == [[1, 0], [1, 0]]
    safe = [[0] * 2 for _ in range(2)]
    safe[0][0] = 1
    assert safe == [[1, 0], [0, 0]]

    point = (1, 2)
    assert point[0] == 1
    box = ([1],)
    box[0].append(2)
    assert box == ([1, 2],)

    scores = {"ada": 10}
    scores["grace"] = 9
    assert list(scores) == ["ada", "grace"]
    assert scores.get("linus") is None

    numbers = {1, 1, 2}  # noqa: B033
    assert numbers == {1, 2}
    try:
        _ = {[1]}  # type: ignore[unhashable]
    except TypeError:
        pass
    else:
        raise AssertionError("list 不能做 set 元素")
    print("ok a08")


if __name__ == "__main__":
    main()
