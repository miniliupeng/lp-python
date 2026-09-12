# 阶段 06: 现代类型系统与 Pydantic V2

现代 Python 开发早已告别“动态类型全靠跑”的蛮荒时代。本阶段聚焦现代类型注解体系（PEP 484/585/604）、基于 Protocol 的结构化类型（鸭子类型）以及驱动全行业数据验证事实标准的 Pydantic V2 Rust 核心引擎。

---

## 💡 核心工程心智与底层机制

1. **现代类型注解演进（PEP 585 / PEP 604）**：
   - 彻底废弃历史陈旧的 `typing.List`、`typing.Dict`、`typing.Union`；
   - 全面拥抱原生容器类型参数化（`list[str]`、`dict[str, int]`）与极简联合操作符（`str | None`），提升可读性并降低导入开销。
2. **Protocol 结构化子类型（Duck Typing 契约）**：
   - 区别于名义子类型（Nominal Subtyping，强制继承抽象基类 ABC）；
   - `typing.Protocol` 实现了静态类型检查阶段的“鸭子类型”验证——只要对象具备相应的方法与签名即可匹配，实现彻底的依赖反转与接口解耦。
3. **Pydantic V2 Rust 核心验证引擎（pydantic-core）**：
   - V2 版本彻底推翻 V1 的纯 Python 实现，核心验证链路全部下沉至 Rust 编写的 `pydantic-core`，数据解析性能暴涨 5~20 倍；
   - 区分 `field_validator`（单字段前置/后置逻辑）与 `model_validator`（跨字段协同逻辑），提供企业级数据出入参保障。

---

## 🗺️ 阶段专题导航

| 专题目录 | 核心原语 | 关键掌握目标 |
| :--- | :--- | :--- |
| **[01-type-hints-and-protocols](./01-type-hints-and-protocols/)** | 现代类型提示与 Protocol 契约 | 掌握 PEP 585/604 语法、`typing.Protocol` 鸭子契约与 mypy/pyright 质检 |
| **[02-pydantic-v2-core-validation](./02-pydantic-v2-core-validation/)** | Pydantic V2 Rust 核心校验 | 掌握 BaseModel 契约、字段约束、自定义验证器与 JSON Schema 导出 |

---

## 🚀 统一运行验证

```bash
uv run python 06-type-system-and-pydantic/01-type-hints-and-protocols/main.py
uv run python 06-type-system-and-pydantic/02-pydantic-v2-core-validation/main.py
```
