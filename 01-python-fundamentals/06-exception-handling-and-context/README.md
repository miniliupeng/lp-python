# 06-exception-handling-and-context: 异常分层体系与上下文协议

## 一、核心机制与设计哲学

- **Python 哲学：EAFP（Easier to Ask for Forgiveness than Permission）**：
  - 传统 C/Go 倾向于 LBYL（Look Before You Leap，先检查指针/键是否存在再访问）；
  - Python 推荐 EAFP（“先做，出错再捕获”）。因为在动态并发环境中，检查与执行之间存在竞态条件（TOCTOU），直接捕获异常不仅代码更凝练，在正常高频路径下还省去了前置条件检查的 CPU 开销。
- **完整的异常控制流生命周期**：
  - `try`：执行可能出错的风险代码块；
  - `except SpecificException as err`：精确捕获并处理目标异常；
  - `else`：**仅在 `try` 块内未抛出任何异常时执行**（适合放置依赖 `try` 成功但本身不应被捕获的业务逻辑）；
  - `finally`：**无论是否抛出异常、是否命中 `return`，均保证最终执行**（资源释放的终极屏障）。
- **上下文管理器协议（Context Manager Protocol）**：
  - 基于 `__enter__()` 与 `__exit__(exc_type, exc_val, exc_tb)`，为任意系统资源提供严格确定性的生命周期管理（RAII 范式）。

## 二、生产规范与避坑指南

1. **严禁裸写 `except:` 或盲目捕获 `except Exception:`**：这会隐式吞掉 `KeyboardInterrupt`（Ctrl+C）、`SystemExit` 等系统退出信号，导致容器和进程无法优雅停机。生产中必须捕获精确的异常基类。
2. **异常链追踪（Exception Chaining）**：在转换或封装业务异常时，必须使用 `raise NewError() from err`，保留原始异常调用栈，杜绝生产排错时的“上下文丢失”。
3. **上下文管理器中的异常吞吐**：在 `__exit__` 中，只有返回 **显式的 `True`** 时，当前异常才会被静音吞掉；返回其他任何值或 `None`，异常都会继续向外层冒泡。

## 三、典型工程示例解析

查看同目录下 `main.py`：
- 演示完整的 `try-except-else-finally` 时序控制流；
- 演示自定义领域异常与 `from err` 异常链保留；
- 演示基于类的自定义上下文管理器与资源确定性释放。
