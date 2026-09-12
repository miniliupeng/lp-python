# 专题 02：FastAPI 核心灵魂 Depends 依赖注入系统与生命周期管理

如果说 Starlette 是 FastAPI 的骨架，Pydantic 是血肉，那么 **`Depends` 依赖注入系统** 就是它的核心灵魂。通过 `Depends`，FastAPI 实现了控制反转（IoC），将用户认证、权限鉴权（RBAC）、数据库会话事务以及请求级缓存以**声明式有向无环图（DAG）**优雅组装，并且利用 **`yield`** 实现了资源确定性的闭环清理。

---

## 一、 痛点驱动：中间件上下文传递的弱类型与资源泄漏

1. **传统中间件字典传参（`request.state.user`）的类型黑盒**：
   - 在旧版框架中，鉴权中间件解析完用户后只能塞入全局或 `request.state` 字典；Controller 内部提取时没有任何代码补全和静态类型检查，极其容易因拼写错误引发 `KeyError`；
2. **跨层数据库事务无法优雅回滚与关闭**：
   - 每个路由函数都必须手动 `try-finally` 处理数据库事务，一旦某个路由中途抛错遗漏捕获，数据库连接将发生致命泄漏。

---

## 二、 机制解密：子依赖树（DAG）解析与 yield 上下文

```text
[ FastAPI Depends 有向无环图解析时序 ]
  路由声明: endpoint(user=Depends(get_current_user), db=Depends(get_db_session))
         │
         ▼ (拓扑排序，并发或顺序解析依赖)
  1. 依赖节点 A: get_db_session()
         ├── yield 前: 开启数据库连接 session
         │
         ▼ (将依赖结果注入下游)
  2. 依赖节点 B: get_current_user(token=Header(...), db=Depends(get_db_session))
         │   └── 自动复用已生成的同一个 db 会话 (默认 use_cache=True)
         ▼
  3. 执行核心业务路由函数 endpoint(user, db)
         │
         ▼ (响应已发送给客户端后，原路折返执行清理)
  4. 回到 get_db_session 的 yield 之后:
         └── 自动执行 session.commit() / session.close()
```

1. **有向无环图自动拓扑解析**：
   - 依赖项可以依赖其他子依赖（多级嵌套），FastAPI 在启动或请求到达时自动构建并扁平化执行该依赖树；
2. **`yield` 的清理保证**：
   - 只要依赖函数使用了 `yield`，哪怕路由内部抛出未捕获异常崩溃，FastAPI 的异常隔离层也会保证 `yield` 后的代码得到执行，安全关闭外部连接。

---

## 三、 生产规范与最佳实践

- **权限认证与数据库会话必须通过 `Depends` 注入**：坚决杜绝在路由内部全局单例取连接；
- **利用 `use_cache=True`（默认行为）共享请求级上下文**：确保单次 HTTP 请求链路中所有层级使用的是同一个数据库事务实例。
