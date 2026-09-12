# 专题 03：现代 ASGI 生命周期 lifespan、洋葱中间件与全局异常兜底

在微服务容器化与云原生部署中，服务的**优雅停机（Graceful Shutdown）**与**统一全局拦截治理**是高可用架构的生命线。现代 FastAPI / Starlette 彻底废弃了旧版容易产生竞态条件的 `on_event("startup")`，全面拥抱标准的 **`lifespan` 异步上下文生命周期**，并结合洋葱模型中间件（Middleware）与全局异常处理器（Exception Handlers），实现生产级全链路可观测性与安全防御。

---

## 一、 痛点驱动：服务启停竞态死锁与未捕获异常敏感泄露

1. **服务启动与关闭的资源竞态（Startup/Shutdown Race）**：
   - 旧版 `on_event("startup")` 无法方便地跨启停共享变量；在 Kubernetes 滚动更新发送 `SIGTERM` 时，容易在后台长任务尚未处理完前强制终止进程，导致事务中断损坏；
2. **未捕获异常泄露内部代码堆栈（Traceback Leakage）**：
   - 如果未配置全局兜底拦截器，Python 默认抛出的 500 页面会将内部数据库表名、SQL 语句和服务器文件路径全量暴露给前端客户端，引发严重黑客攻击渗透风险。

---

## 二、 机制解密：lifespan 异步上下文与洋葱中间件执行流

```text
[ 现代 lifespan 生命周期拓扑 ]
  @asynccontextmanager
  async def lifespan(app: FastAPI):
      # 【启动期 Setup】: 预热连接池、加载 AI 向量模型权重、注册服务发现 Consul/Nacos
      yield
      # 【停机期 Teardown】: 拒收新请求、消费完在途队列数据、安全断开连接池优雅退出

[ 洋葱模型中间件流转 (BaseHTTPMiddleware) ]
  客户端请求 ──> [ 中间件前置: 注入 TraceId, 记录 start_time ]
                       │
                       ▼
                 [ 进入路由处理函数业务逻辑 ]
                       │
                       ▼
  客户端响应 <── [ 中间件后置: 计算总耗时, 挂载 X-Process-Time 响应头 ]
```

1. **标准的 `lifespan` 异步生成器**：
   - 严格遵循 Python `contextlib.asynccontextmanager` 协议，保证从启动到优雅关闭的生命周期完全对称；
2. **全局异常处理器兜底拦截（Fail-Safe）**：
   - 捕获基类 `Exception`，在服务端输出完整日志，并对外返回标准结构化 JSON（统一包含 `code`, `message`, `trace_id`），杜绝敏感堆栈泄露。

---

## 三、 生产规范与最佳实践

- **永远配置统一全局统一 JSON 错误结构**；
- **耗时打点必须使用单调时钟 `time.perf_counter()`**：避免系统管理员手动校时（NTP 同步）引发负耗时 Bug。
