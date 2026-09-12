# 大厂高频面试题精讲 (07-03-fastapi-lifespan-and-middlewares)

---

### Q1: 为什么 FastAPI 官方废弃了 @app.on_event("startup") 和 "shutdown"，全面推崇 lifespan 上下文管理器？

#### 🎯 面试官考点
- ASGI 规范演进（ASGI Lifespan Protocol）、资源跨启停状态共享与异常安全。

#### 💡 满分回答模板
1. **历史 `on_event` 的严重痛点**：
   - **状态割裂**：`startup` 和 `shutdown` 是两个完全分离的独立回调函数，如果要在 `startup` 初始化连接池并在 `shutdown` 关闭，必须借助于全局变量（Global Variables）跨函数传递，破坏封装性；
   - **错误处理脆弱**：如果 `startup` 中途初始化失败抛出异常，`shutdown` 事件通常不会被可靠触发，容易引发资源悬挂。
2. **`lifespan` 异步上下文管理器的决定性优势**：
   - 严格基于标准 `@asynccontextmanager`：
     ```python
     @asynccontextmanager
     async def lifespan(app: FastAPI):
         db = await init_db()  # 启动前
         yield {"db": db}  # 运行期间在 state 中共享
         await db.close()  # 退出时在同一作用域保证必定执行
     ```
   - 启停代码天然处于同一词法作用域内，状态流转对称清晰，并且可以利用 `state` 安全挂载全局单例，完全符合最新 ASGI Lifespan 协议标准。

---

### Q2: FastAPI 的中间件模型（BaseHTTPMiddleware）在底层执行流程上是线性模型还是洋葱模型？

#### 🎯 面试官考点
- 中间件架构对比（Express vs Koa vs ASGI）、执行流时序与双向拦截能力。

#### 💡 满分回答模板
1. **执行流本质：双向环形洋葱模型（Onion Model）**：
   - FastAPI / Starlette 的 HTTP 中间件模型在本质上是标准的**洋葱模型**（类似 Koa）；
   - 每个中间件以 `response = await call_next(request)` 为分水岭；
2. **双向拦截时序**：
   - **请求到达时（由外向内）**：最外层中间件的前半段先执行（如提取请求头、注入 TraceId、记录开始时间戳）；
   - 控制权层层交接直至最终进入核心路由函数；
   - **响应返回时（由内向外原路折返）**：路由执行完毕后，中间件按相反顺序逐层执行后半段后置逻辑（如计算全链路耗时、压缩响应体、挂载自定义安全响应头 `X-Process-Time`）。

---

### Q3: 在生产环境中，全局异常捕获器（Exception Handlers）应该如何设计，以防范未捕获异常泄漏内部敏感堆栈？

#### 🎯 面试官考点
- Web 安全红线（Information Disclosure 敏感信息泄露防御）、全链路可观测性排错设计。

#### 💡 满分回答模板
1. **防范敏感信息泄漏（信息安全红线）**：
   - 未捕获的系统级异常（如数据库连接断开、SQL 语法错误、第三方 API 报错）往往在 Traceback 中包含数据库物理 IP、用户密码、SQL 查询表结构等敏感信息；
   - 全局兜底拦截器必须捕获顶级基类 **`Exception`**，在响应中对客户端屏蔽任何技术细节，统一返回脱敏的友好错误信息。
2. **生产级“三位一体”标准异常响应设计**：
   - **内部精准报警**：在拦截器内部，将包含完整 Traceback 的真实错误通过日志框架（结合 Sentry 等 APM）上报；
   - **携带全链路 `trace_id`**：在返回给前端的 JSON 中必须包含一个唯一的追踪 ID（如 `{"code": 500, "message": "服务异常", "trace_id": "xxx"}`）；
   - 用户在界面遇到报错只需提供 `trace_id`，值班工程师凭此 ID 即可在日志中心秒级检索到当时的真实崩溃堆栈，兼顾了安全性与排障效能。
