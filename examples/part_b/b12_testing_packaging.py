"""用标准库 unittest 测一个纯函数，并用 tomllib 读一份项目声明。"""

from __future__ import annotations

import tomllib
import unittest

SAMPLE_PYPROJECT = """
[project]
name = "gradebook"
requires-python = ">=3.12"
dependencies = []
"""


def clip(value: int, low: int, high: int) -> int:
    if low > high:
        raise ValueError("low 不能大于 high")
    return max(low, min(high, value))


class ClipTests(unittest.TestCase):
    def test_inside(self) -> None:
        self.assertEqual(clip(2, 0, 5), 2)

    def test_high(self) -> None:
        self.assertEqual(clip(9, 0, 5), 5)

    def test_bad_range(self) -> None:
        with self.assertRaises(ValueError):
            clip(1, 5, 0)


def main() -> None:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ClipTests)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    assert result.wasSuccessful()
    data = tomllib.loads(SAMPLE_PYPROJECT)
    assert data["project"]["requires-python"] == ">=3.12"
    assert data["project"]["name"] == "gradebook"
    print("ok b12")


if __name__ == "__main__":
    main()
