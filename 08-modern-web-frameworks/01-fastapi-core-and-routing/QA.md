# 大厂高频面试题精讲 (07-01-fastapi-core-and-routing)

---

### Q1: 为什么 FastAPI 在高并发吞吐量基准测试中远超传统的 Flask 与 Django？底层做了哪些性能优化？

#### 🎯 面试官考点
- 现代 Web 框架架构演进、ASGI 异步非阻塞模型与 Pydantic V2 Rust 引擎加速。

#### 💡 满分回答模板
1. **ASGI 异步事件驱动架构 vs WSGI 同步模型**：
   - 传统 Flask/Django 建立在同步 WSGI 规范之上，处理每个连接必须独占一个操作系统线程/进程。面对万级并发长连接时，线程上下文切换与内存暴涨成为致命瓶颈；
   - FastAPI 建立在 **Starlette (ASGI)** 规范之上，天然运行于单线程异步事件循环中，通过非阻塞 Socket 复用处理成千上万并发请求，资源开销低两个数量级。
2. **Rust 原生加速的数据解析引擎（Pydantic V2）**：
   - 过去 Python Web 框架在反序列化 JSON 和参数校验时，需要创建海量临时 Python 对象；
   - FastAPI 将数据校验与序列化全生命周期委托给用 **Rust 编写的 `pydantic-core`**，在 C 语言内存紧凑空间完成单次扫描校验，性能提升 5~17 倍。

---

### Q2: 什么是 WSGI 与 ASGI？它们在 Python Web 服务器演进中扮演了什么角色？

#### 🎯 面试官考点
- Python Web 网关接口协议标准演进（PEP 3333 vs ASGI 规范）、长连接与流式支持。

#### 💡 满分回答模板
1. **WSGI（Web Server Gateway Interface, PEP 3333）**：
   - **设计时代**：针对传统的“单请求-单响应”同步阻塞 Web 模型；
   - **核心函数签名**：`application(environ, start_response)`；
   - **局限**：天然不支持长连接、异步 I/O、WebSocket 双向通信与 Server-Sent Events (SSE) 流式打字机响应。
2. **ASGI（Asynchronous Server Gateway Interface）**：
   - **设计时代**：面向现代全双工、高并发异步驱动环境；
   - **核心函数签名**：`async def app(scope, receive, send):`；
   - **架构收益**：通过 `receive()` 和 `send()` 两个异步消息管道，原生统一支持 HTTP、WebSocket、流式传输与长时间运行任务，是现代高吞吐全栈网关的绝对标准。

---

### Q3: 在 FastAPI 路由定义中，async def endpoint() 与普通 def endpoint() 在底层调度上有何本质区别？

#### 🎯 面试官考点
- 框架底层线程池代理机制、错误使用导致事件循环冻结的防范策略。

#### 💡 满分回答模板
1. **`async def` 路由（主线程事件循环直接执行）**：
   - FastAPI 直接将该路由作为原生协程放入**主事件循环**中调度；
   - **红线**：内部必须全部使用非阻塞异步代码（`await`）。如果误在其中调用了阻塞调用（如 `time.sleep`），将直接冻结整个服务的主循环！
2. **普通 `def` 路由（后台线程池自动卸载）**：
   - FastAPI 会通过 **`anyio.to_thread.run_sync()` 自动将其派发到外部专用线程池（ThreadPool）中执行**；
   - **适用场景**：如果现有老旧业务代码重度依赖同步数据库驱动或未异步化的 SDK，声明为普通 `def` 可以防止主循环被阻塞，兼具安全性与迁移兼容性。
