.PHONY: help sync lint fmt test clean run-all

help:
	@echo "🛠️ lp-python 现代工程效能工具箱:"
	@echo "  make sync      - 使用 uv 极速安装并同步纯净虚拟环境"
	@echo "  make lint      - 使用 ruff 执行静态代码与质量检查"
	@echo "  make fmt       - 使用 ruff 自动格式化代码"
	@echo "  make test      - 使用 pytest 运行现代化自动化测试"
	@echo "  make run-all   - 串行执行全量 28 个主代码文件"
	@echo "  make clean     - 清理 Python 编译缓存与临时产物"

sync:
	uv sync

lint:
	uv run ruff check .

fmt:
	uv run ruff format .
	uv run ruff check --fix .

test:
	uv run pytest -v 00-toolchain-and-engineering-primer/03-pytest-native-testing/test_calc.py tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.db" -delete

run-all:
	@for f in $$(find . -name "main.py" -not -path "*/.*" | sort); do \
		echo "🚀 正在执行: $$f"; \
		uv run python "$$f" || exit 1; \
	done
	@echo "✅ 全量主程序验证执行通过！"
