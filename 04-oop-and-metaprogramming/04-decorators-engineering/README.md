# 专题 04：企业级函数装饰器、带参装饰器工厂与 functools.wraps 元数据工程

在现代 Python 架构中，**装饰器（Decorators）**是实现切面编程（AOP）、请求耗时统计、分布式锁注入、权限 RBAC 拦截与统一缓存的利器。然而，粗糙手写的装饰器会导致被装饰函数的 `__name__`、类型注解与签名在反射时丢失，破坏 API 框架与单元测试。本专题深入探讨工业级可复用装饰器的标准构建模式。

---

## 一、 痛点驱动：装饰器元数据擦除与洋葱层时序错乱

1. **元数据擦除（Function Metadata Erasure）**：
   - 装饰器本质是返回一个新的内部闭包函数（Wrapper）；
   - 若不处理元数据，所有被装饰函数的名字都将变成 `"wrapper"`，docstring 变为空，导致 FastAPI、Sphinx 文档生成器与 Sentry 报错追踪全部失效；
2. **带参装饰器的认知混淆**：
   - 面对需要配置参数的装饰器（如 `@retry(times=3)`），层级嵌套设计错误导致传参逻辑混乱。

---

## 二、 机制解密：装饰器执行时序与 functools.wraps

```text
[ 叠放装饰器的编译与调用时序 ]
  @decorator_a
  @decorator_b
  def target_fn(): ...

  编译装载期 (从下向上包裹): target_fn = decorator_a(decorator_b(target_fn))
  实际执行期 (从外向内调用): 先进入 decorator_a 的前置逻辑 -> 再进入 decorator_b -> 执行 target_fn
```

1. **`functools.wraps` 的反射修补底层**：
   - 通过调用 `WRAPPER_ASSIGNMENTS` 与 `WRAPPER_UPDATES`，自动将被包裹函数的 `__name__`, `__doc__`, `__annotations__`, `__module__` 逐一复制，并挂载 **`__wrapped__`** 指向原函数；
2. **带参装饰器（三层闭包函数工厂）**：
   - 最外层：接收装饰器参数；
   - 中间层：接收被装饰的目标函数；
   - 最内层：接收真实调用时的参数并执行 AOP 拦截。

---

## 三、 生产规范与最佳实践

- **永远无条件加上 `@functools.wraps(func)`**；
- **参数解包保持通用透明**：内层 wrapper 必须声明为 `def wrapper(*args: Any, **kwargs: Any) -> Any:` 并完整透传。
