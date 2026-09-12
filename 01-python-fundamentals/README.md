# 阶段 01: Python 语法基础与核心范式

本阶段是整个 `lp-python` 教程体系的**入门基石**。本阶段严格对齐企业级工业规范，帮助零基础、跨语言或准备面试的工程师以最高效路径掌握 Python 3.12+ 的核心语法与编程范式。

---

## 💡 核心工程心智与底层机制

1. **动态强类型与引用绑定模型**：
   - Python 是典型的**动态强类型语言**（变量无类型，对象有类型）；
   - 赋值本质是名字到堆内存对象指针的绑定操作；金融高精度业务必须使用 `Decimal` 彻底杜绝 IEEE 754 浮点误差。
2. **逻辑短路求值与对象同一性**：
   - 彻底区分对象同一性比较（`is` 比对内存物理地址）与值相等性比较（`==` 调用 `__eq__` 协议）；
   - 深刻理解 `and` / `or` 的短路返回值机制与海象运算符（`:=`）的单次求值复用优化。
3. **现代控制流与优雅防御**：
   - 掌握 `for-else` 语法原语，消除繁琐的布尔状态标志位；
   - 警惕迭代中就地 `remove` / `pop` 导致的索引跳跃陷阱，践行不可变与推导式过滤哲学。
4. **函数签名与参数解构安全性**：
   - 规避初学者最常踩的“默认可变参数（Mutable Default Arguments）在函数定义时静态单例求值”陷阱；
   - 掌握现代 PEP 570 位置专用（`/`）与关键字专用（`*`）强制规范，保障团队 API 契约稳定性。
5. **核心容器内存开销与推导式**：
   - 剖析 list（连续动态数组）、dict（散列表）、set 的底层时间复杂度；
   - 深刻理解推导式（内存即时分配）与生成器表达式（流式惰性计算）在海量数据场景下的内存表现。
6. **EAFP 哲学与异常上下文链**：
   - 贯彻 Python 官方推崇的“请求宽恕容易过请求许可（EAFP）”哲学；
   - 利用 `raise ... from ...` 显式追溯根本异常原因，通过 `__enter__` / `__exit__` 确保外部资源的确定性析构。

---

## 🗺️ 阶段专题导航

| 专题目录 | 核心原语 | 关键掌握目标 |
| :--- | :--- | :--- |
| **[01-data-types-and-variables](./01-data-types-and-variables/)** | 引用绑定与数据类型 | 动态强类型、对象内存指针绑定、IEEE 754 浮点误差与 Decimal 生产选型 |
| **[02-operators-and-expressions](./02-operators-and-expressions/)** | 短路逻辑与对象同一性 | 对象同一性（`is`）与值相等（`==`）、逻辑短路返回值机制、海象运算符（`:=`） |
| **[03-control-flow-statements](./03-control-flow-statements/)** | 现代流程控制与陷阱防御 | for-else 优雅搜索机制、循环中就地修改陷阱、现代控制流 |
| **[04-functions-and-signatures](./04-functions-and-signatures/)** | 传引用本质与高级签名 | 传对象引用本质、默认可变参数陷阱与 None 哨兵、位置专用（`/`）与关键字专用（`*`）签名 |
| **[05-core-containers-and-comprehensions](./05-core-containers-and-comprehensions/)** | 四大容器与推导式内存 | 容器底层原理、推导式与生成器表达式内存模型对比、deque 高性能队列 |
| **[06-exception-handling-and-context](./06-exception-handling-and-context/)** | 异常分层与上下文协议 | EAFP 哲学、try-except-else-finally 完整控制流、__enter__/__exit__ 上下文管理协议 |

---

## 🚀 统一运行验证

```bash
uv run python 01-python-fundamentals/01-data-types-and-variables/main.py
uv run python 01-python-fundamentals/02-operators-and-expressions/main.py
uv run python 01-python-fundamentals/03-control-flow-statements/main.py
uv run python 01-python-fundamentals/04-functions-and-signatures/main.py
uv run python 01-python-fundamentals/05-core-containers-and-comprehensions/main.py
uv run python 01-python-fundamentals/06-exception-handling-and-context/main.py
```
