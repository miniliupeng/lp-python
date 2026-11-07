# 现代 Python 工业级后端核心架构与实战教程 (lp-python)

面向 2026 最新行业标准的现代 Python (3.12+) 体系化教程。严格对齐 **广度全面**、**极速入门**、**面试就职** 三大战略支柱，对标 Go 语言兄弟项目打造全栈后端闭环。

---

## 🌟 三大战略支柱

1. **🌱 极速入门（Fundamentals First）**：
   - 包含从零起步的 `01-python-fundamentals` 语法全解析；
   - 彻底吃透基础数据类型、运算符短路、for-else 控制流、函数参数解构、核心容器与异常分层体系，跨语言开发者与零基础工程师可无痛平滑上手。
2. **🌐 广度全栈（End-to-End Breadth）**：
   - 从现代包管理工具链（uv）到 CPython 内存模型、GC 与垃圾回收；
   - 从 OOP 描述符与装饰器到异步并发（asyncio/TaskGroup）；
   - 从现代类型系统（Pydantic V2）到异步存储层（SQLAlchemy 2.0 / Redis）；
   - 从现代企业级 Web（FastAPI DI & Lifespan）到最新 AI 原语（RAG、MCP 与 SSE 流式全栈）。
3. **🎯 面试就职（Interview-Ready Engineering）**：
   - **黄金 50~80 行代码法则**：拒绝动辄数百行的全功能巨石代码，每个专题精控在 50~80 行，一眼看透核心原语，5 分钟可手写默写；
   - **工程三段式深度解析**：彻底剔除低幼生活化比喻，坚持痛点驱动、CPython 内核机制解密与架构选型权衡；
   - **大厂高频面试真题库**：全量配备“🎯 面试官考点 + 💡 满分回答模板”，结构化分点陈述，直击高频淘汰线。

---

## 🗺️ 全套 10 大阶段架构导航 (38 个精炼专题)

| 阶段编号 | 阶段主题 | 专题数 | 核心技术要点与定位 |
| :--- | :--- | :---: | :--- |
| **00** | [工程效能与现代工具链](./00-toolchain-and-engineering-primer/) | 4 | uv 极速包管理、pyproject.toml 声明式构建、pytest 测试、.env 统一配置 |
| **01** | [Python 语法基础与核心范式](./01-python-fundamentals/) | 6 | 数据类型与 Decimal 精度、运算符短路、for-else 控制流、函数签名、容器推导式、异常上下文 |
| **02** | [底层对象模型与内存机制](./02-python-data-model-and-memory/) | 4 | PyObject 结构、深浅拷贝与内存逃逸、小整数池与不可变驻留、分代 GC 与循环引用 |
| **03** | [现代控制流与函数式编程](./03-control-flow-and-functional/) | 4 | match-case 模式匹配、函数一等公民与作用域、迭代器协议、生成器与协程基石 |
| **04** | [面向对象、元编程与装饰器](./04-oop-and-metaprogramming/) | 5 | \`__new__\` vs \`__init__\`、魔术方法、描述符协议与 property、装饰器进阶、MRO 与多继承 |
| **05** | [并发编程、GIL 与现代 Asyncio](./05-concurrency-and-asyncio/) | 4 | 多线程/多进程与 GIL 限制、事件循环核心机制、TaskGroup 结构化并发、异步信号量与池化 |
| **06** | [现代类型系统与 Pydantic V2](./06-type-system-and-pydantic/) | 2 | PEP 484/585/604 类型注解与 Protocol、Pydantic V2 Rust 核心验证与序列化 |
| **07** | [存储层、持久化与异步 ORM](./07-data-layer-and-storage/) | 3 | aiosqlite 预编译防注入、SQLAlchemy 2.0 异步 Session、Redis 高并发缓存与雪崩治理 |
| **08** | [现代 Web 框架 FastAPI 企业级实践](./08-modern-web-frameworks/) | 3 | 路由树与 Pydantic 参数绑定、三层依赖注入 (DI) 系统、Lifespan 生命周期与中间件 |
| **09** | [AI 原语、智能体与全栈工程实战](./09-ai-primitives-and-capstone/) | 3 | 纯原生向量检索与 RAG、MCP 智能体工具调用编排、SSE 流式响应与全栈大作业 |

---

## 🛠️ 极速开箱体验

本项目使用现代极速包管理器 `uv` 进行环境管理：

```bash
# 1. 极速同步纯净依赖与虚拟环境
make sync

# 2. 代码静态风格与质量检查 (Ruff)
make lint

# 3. 运行自动化测试套件 (Pytest)
make test

# 4. 一键串行验证执行所有 38 个专题代码
make run-all
```

---

## 📚 延伸指南
- 详见 [learning-guide.md](./learning-guide.md) 获取学习路径与备战大厂面试策略。
- 详见 [PROGRESS.md](./PROGRESS.md) 追踪全量 38 个专题的代码行数与交付状态。
