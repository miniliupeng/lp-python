# 阶段 00: 现代工程工具链与开发基石

工欲善其事，必先利其器。在深入 Python 语言内核与业务架构之前，必须先理清现代 Python 后端工程的工具链基石：**如何以最轻量、最现代、最高效的方式构建、运行与测试 Python 代码**。

---

## 💡 核心工程心智与工具演进

1. **Python 3.12+ 现代运行时**：
   - 全面拥抱现代 CPython 运行时特性（PEP 695 类型参数语法、PEP 684 隔离解释器、改进报错回溯与性能提升）；
   - 摆脱历史遗留的 Python 2/3 过渡包袱，建立纯净现代后端工程认知。
2. **uv 极速包管理与虚拟环境拓扑**：
   - 基于 Rust 编写的下一代超高速包管理器 `uv`（较传统 pip/pipenv 快 10~100 倍）；
   - 具备全局依赖内容寻址缓存机制，彻底解决多项目重复下载耗时与依赖污染问题。
3. **pyproject.toml 声明式构建**：
   - 彻底废弃历史遗留、易引发供应链远程代码执行漏洞的 `setup.py` 与割裂的 `requirements.txt`；
   - 严格遵循 PEP 517/518/621 标准，使依赖、版本、项目元数据与构建后端全部收敛于单一真理来源。
4. **pytest 原生测试体系**：
   - 拒绝笨重复杂的第三方断言库，采用简洁强大的原生 Python `assert` 表达式与强大的参数化驱动（`@pytest.mark.parametrize`）；
   - 结合 Fixture 机制实现测试依赖的确定性生命周期治理。
5. **配置与环境变量安全治理**：
   - 严格遵循云原生十二要素应用规范（12-Factor App），将配置与代码物理分离；
   - 结合 `.env` 规范实现环境无感知加载，杜绝密钥硬编码入库安全事故。

---

## 🗺️ 阶段专题导航

| 专题目录 | 核心原语 | 关键掌握目标 |
| :--- | :--- | :--- |
| **[01-uv-and-python-runtime](./01-uv-and-python-runtime/)** | uv 极速管理与虚拟环境 | 掌握 uv 虚拟环境创建、依赖极速锁定与全局缓存机制 |
| **[02-modern-pyproject-and-toolchain](./02-modern-pyproject-and-toolchain/)** | pyproject.toml 声明式构建 | 搞懂 PEP 517/518/621 标准，实现构建后端与依赖统一声明 |
| **[03-pytest-native-testing](./03-pytest-native-testing/)** | 原生断言与参数化测试 | 掌握 pytest 灵活断言、异常拦截与 Fixture 注入机制 |
| **[04-env-and-configuration](./04-env-and-configuration/)** | 十二要素配置安全治理 | 掌握 python-dotenv 环境隔离与敏感密钥生产级治理 |

---

## 🚀 统一运行验证

```bash
uv run python 00-toolchain-and-engineering-primer/01-uv-and-python-runtime/main.py
uv run python 00-toolchain-and-engineering-primer/02-modern-pyproject-and-toolchain/main.py
uv run pytest 00-toolchain-and-engineering-primer/03-pytest-native-testing/test_calc.py
uv run python 00-toolchain-and-engineering-primer/04-env-and-configuration/main.py
```
