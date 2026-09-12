# 专题 02：pyproject.toml 声明式工程标准与 Ruff 极速代码治理

在早期 Python 项目中，工程配置割裂在 `setup.py`、`setup.cfg`、`requirements.txt`、`Pipfile`、`tox.ini` 等十几个异构文件中。现代 Python 通过 **PEP 518 / PEP 621** 确立了以 **`pyproject.toml`** 为唯一真理来源的声明式工程标准，并由基于 Rust 的超高性能工具 **`Ruff`** 全面统一了代码格式化与静态检查。

---

## 一、 痛点驱动：异构配置与静态检查工具链碎片化

1. **`setup.py` 的可执行代码安全漏洞与构建不可预测性**：
   - `setup.py` 本身是一段动态执行的 Python 脚本，获取依赖或元数据必须运行不受信代码，带来严重供应链攻击风险；
2. **传统 Linter 冗余与速度瓶颈**：
   - 过去大型项目需要同时安装 Flake8（语法风格）、Black（代码格式化）、isort（导入排序）、Bandit（安全扫描）；
   - 各工具重复解析生成 AST 抽象语法树，在大规模代码库中执行检查耗时动辄数分钟，极大阻塞 CI/CD 门禁。

---

## 二、 机制解密：声明式元数据与 Ruff 单次 AST 遍历

```text
[ pyproject.toml ] 统一声明式标准
 ├── [project]            ── 规范核心元数据 (name, version, dependencies)
 ├── [tool.ruff]           ── 静态规则与代码治理 (一行替代 flake8+black+isort)
 └── [tool.pytest.ini_options] ── 测试运行配置
```

1. **声明式驱动（Declarative Driven）**：
   - `pyproject.toml` 采用标准 TOML 格式，纯静态数据解析，杜绝了执行恶意构造代码的可能性；
2. **Ruff 的单次 AST 解析合并优化（Single-pass Optimization）**：
   - Ruff 完全用 Rust 编写。在执行检查与格式化时，只需**一次词法分析与 AST 语法树遍历**，即可同时完成导入排序重整、死代码清理、弃用语法提示和格式对齐，速度比传统 Python 脚本工具快 **10 ~ 100 倍**。

---

## 三、 生产规范与最佳实践

- **依赖语义分层**：
  - 核心业务运行必须依赖声明在 `[project.dependencies]`；
  - 开发、测试、代码扫描等辅助依赖严格放置在 `[dependency-groups.dev]`，防止打包部署时容器镜像体积膨胀。
- **配置固化到版本控制**：
  - 必须将 `pyproject.toml` 与 `uv.lock` 一同纳入 Git 提交，坚决杜绝未锁定版本导致的“线上依赖飘移事故”。
