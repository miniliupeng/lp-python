# 专题 01：FastAPI 异步内核、ASGI 架构与 APIRouter 模块化设计

在现代 Python Web 后端生态中，**FastAPI** 已成为事实上的工业标准。相比传统基于同步 WSGI 规范的 Django 和 Flask，FastAPI 全面拥抱 **ASGI 异步网关规范**，以 **Starlette** 为极速异步路由底座、以 **Pydantic V2 (Rust core)** 为数据契约引擎，实现了与 NodeJS / Go 逼近的高性能并发吞吐，并原生提供声明式 OpenAPI (Swagger) 文档生成能力。

---

## 一、 痛点驱动：传统 WSGI 的并发吞吐瓶颈与文档撕裂

1. **WSGI 同步多进程模型的线程瓶颈**：
   - 传统 Flask/Django 运行在 Gunicorn+WSGI 模式下，一个 Worker 进程在处理一个阻塞网络调用时无法分发其他请求，维持数千个并发长连接（如 SSE / WebSocket）会导致服务器内存与进程资源耗尽；
2. **接口代码与 Swagger 文档维护严重撕裂**：
   - 过去后端开发完 API，必须在外部手动编写复杂的 YAML 文档，线上字段一旦变更，文档往往落后不同步，引发联调灾难。

---

## 二、 机制解密：ASGI 事件驱动与 APIRouter 前缀分发

```text
[ 现代 ASGI Web 服务器分层 ]
  客户端 HTTP 请求
         │
         ▼
  Uvicorn (基于 uvloop 的底层超高性能 ASGI 服务器)
         │
         ▼
  FastAPI 引擎 (基于 Starlette 路由树分发)
         ├── Pydantic V2 (Rust 原生并发解析 Request JSON)
         ├── APIRouter 路由前缀树匹配
         └── 自动化生成 OpenAPI /docs 交互式文档
```

1. **ASGI 异步事件协议**：
   - 将每次 HTTP 请求抽象为一个异步可调用对象：`app(scope, receive, send)`；
   - 在等待数据库或外部网络响应时，主循环通过 `await receive()` 挂起当前协程并立即处理其他请求，充分释放 CPU 潜能；
2. **`APIRouter` 模块化解耦**：
   - 允许将大型系统的业务路由（如 `/users`, `/orders`）拆分到独立模块，统一注入公共前缀（prefix）、公共依赖（dependencies）与标签（tags）。

---

## 三、 生产规范与最佳实践

- **路由处理函数根据 I/O 性质选择关键字**：
  - 纯异步 I/O 代码声明为 `async def endpoint():`；
  - 若调用老旧阻塞的第三方库，直接声明为普通 `def endpoint():`（FastAPI 会自动将其放入底层线程池运行，避免阻塞主循环）；
- **响应体显式声明 `response_model`**：严格过滤内部机密字段，杜绝密码散列泄露。
