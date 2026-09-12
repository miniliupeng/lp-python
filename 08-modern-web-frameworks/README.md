# 阶段 08: 现代 Web 框架 FastAPI 企业级实践

FastAPI 是当今 Python 现代化异步微服务的事实标准。本阶段剖析其背后的 ASGI 运行机制、与 Pydantic 深度绑定的声明式路由参数校验、三层依赖注入（DI）系统以及生产级 Lifespan 生命周期管控。

---

## 💡 核心工程心智与底层机制

1. **ASGI 异步网关接口与声明式路由**：
   - 基于 Starlette 与 Uvicorn/ASGI 标准，打破 WSGI 单进程同步阻塞局限；
   - 结合 Pydantic 自动生成符合 OpenAPI (Swagger) 规范的交互式接口文档与强类型输入拦截。
2. **Depends 依赖注入系统（Dependency Injection）**：
   - 具备有向无环图（DAG）自动拓扑排序与依赖结果缓存机制；
   - 通过 `yield` 语法在请求进入时初始化外部连接（如 DB Session、Redis），并在响应返回给客户端后执行确定性析构与归还连接。
3. **Lifespan 生命周期与洋葱中间件（Middlewares）**：
   - 彻底取代已废弃的 `@app.on_event("startup")` / `"shutdown"` 孤立钩子；
   - 采用单一异步上下文管理器统一管控服务初始化资源预热与优雅停机（SIGTERM）；编写符合 ASGI 规范的请求耗时追踪中间件。

---

## 🗺️ 阶段专题导航

| 专题目录 | 核心原语 | 关键掌握目标 |
| :--- | :--- | :--- |
| **[01-fastapi-core-and-routing](./01-fastapi-core-and-routing/)** | 路由解耦与 Pydantic 校验 | 掌握 APIRouter 模块拆分、Path/Query 参数绑定与 422 自动校验 |
| **[02-fastapi-dependency-injection](./02-fastapi-dependency-injection/)** | Depends 依赖树与 yield 析构 | 深入嵌套鉴权子依赖、数据库 Session 请求级生命周期与优雅回滚 |
| **[03-fastapi-lifespan-and-middlewares](./03-fastapi-lifespan-and-middlewares/)** | Lifespan 生命周期与中间件 | 掌握现代 Lifespan 资源预热/优雅停机与全局请求上下文洋葱模型 |

---

## 🚀 统一运行验证

```bash
uv run python 08-modern-web-frameworks/01-fastapi-core-and-routing/main.py
uv run python 08-modern-web-frameworks/02-fastapi-dependency-injection/main.py
uv run python 08-modern-web-frameworks/03-fastapi-lifespan-and-middlewares/main.py
```
