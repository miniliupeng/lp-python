"""用字典和函数汇总一份成绩单。"""

from __future__ import annotations


def average(scores: list[int]) -> float:
    if not scores:
        raise ValueError("成绩不能为空")
    return sum(scores) / len(scores)


def passed(scores: list[int], bar: int = 60) -> list[int]:
    return [score for score in scores if score >= bar]


def report(book: dict[str, list[int]]) -> list[tuple[str, float]]:
    rows = [(name, average(scores)) for name, scores in book.items()]
    return sorted(rows, key=lambda item: (-item[1], item[0]))


def main() -> None:
    book = {"Ada": [80, 90], "Grace": [100], "Lin": [50, 70]}
    assert average(book["Ada"]) == 85
    assert passed(book["Lin"]) == [70]
    assert report(book)[0][0] == "Grace"
    try:
        average([])
    except ValueError:
        pass
    else:
        raise AssertionError("空成绩必须拒绝")
    print("ok a13")


if __name__ == "__main__":
    main()
