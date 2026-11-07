# Python 全景教程：从零基础到 2026 面试

这是一份从零写起的中文教程。读者可以没有编程背景。读完 Part A 能写小脚本；读完 Part B 能读懂日常业务代码；Part C 解释 CPython 怎么执行这些代码；Part D 把语言放到服务和系统设计里；Part E 是对照答案用的题库，不是另一套互相矛盾的口诀。

这个分支只有这份教程：根 `README.md`、`docs/python-tutorial/` 和 `examples/`。它不携带其他专题目录。入口说明和总大纲也写在根 `README.md`。

## 版本假设

| 项目 | 约定 |
| --- | --- |
| 可执行示例 | **CPython 3.12**。本环境验证版本是 3.12.3。语法和标准库调用都不使用 3.13 及以上才有的形式。 |
| 语言叙述的基准 | Python 3.12 的语言参考与标准库行为。 |
| 更高版本 | Python 3.13（2024-10）、3.14（2025-10-07）、3.15（2026-10-09，写作时文档站可见 3.15.2）只在标明版本的段落里出现。 |
| 实现 | 默认说的是 CPython。PyPy 等其他实现不在示例的保证范围内。 |

必须分开的两句话：

- **语言保证**：写进语言参考、换一个符合标准的实现仍然成立。例如 `==` 走相等性比较，`dict` 从 3.7 起按插入顺序迭代。
- **CPython 细节**：只在 CPython 上观察得到，不能当语法规则背。例如 `-5` 到 `256` 的整数缓存、字节码名字、GIL。

2026 年 11 月的运行时结论，后文会展开，这里先定调，避免和旧博客打架：

- 默认的 CPython 构建**仍然有 GIL**。自由线程（free-threaded，PEP 703）在 3.13 是实验构建，在 3.14 起成为官方支持的**可选**构建，不是默认解释器。
- 3.15 的官方 macOS 安装包默认带上自由线程支持。这不等于你敲的 `python` 已经关掉 GIL。3.13 及以上用 `sys._is_gil_enabled()` 看当前进程。
- JIT（PEP 744）到 3.15 仍是实验特性。3.13 默认构建不包含它；3.14 的官方 macOS / Windows 二进制可以用 `PYTHON_JIT=1` 打开。3.14 文档写明自由线程构建不支持 JIT。
- 3.14 才有 t-string（PEP 750）、默认延迟求值注解（PEP 649 / 749）、`concurrent.interpreters`（PEP 734）。
- 3.15 才有 `lazy` 导入（PEP 810）、内置 `frozendict`（PEP 814，**不是** `dict` 的子类）、`sentinel`（PEP 661）、推导式里的 `*` / `**` 解包（PEP 798），以及默认 UTF-8 文本编码（PEP 686）。

## 怎么读

1. 每一章先跑对应示例，再读正文。示例在 `examples/`，用断言固定行为，失败就是教程和解释器不一致。
2. 零基础按 A → B → C → D 的顺序读。不要从 C 开始，那里默认你已经能读写函数和类。
3. 有其他语言经验：A02、A05、A08 解决“名字和容器”的差异，然后从 B 读到 D。
4. 准备面试：C、D 读完再做 E。先盖住答案写出自己的版本，再对照。题库会指出常见的错法，那些错法不要背。
5. 一章里的练习都有参考答案，放在该章末尾。先自己写。

```bash
python examples/run_all.py
```

只跑一章时，直接执行该章给出的文件，例如：

```bash
python examples/part_a/a02_names_and_objects.py
```

示例只依赖标准库，不需要先安装本仓库的 Web 依赖。

## 大纲

### Part A　入门

| 章 | 文件 | 你要掌握的 |
| --- | --- | --- |
| A01 | [安装、运行与执行模型入门](part-a/a01-install-and-run.md) | 安装、脚本、REPL、`python -m`、编译成字节码再执行 |
| A02 | [名字、对象与类型](part-a/a02-names-objects-types.md) | 赋值是绑定，动态类型，强类型 |
| A03 | [数字、布尔与 None](part-a/a03-numbers-bool-none.md) | `int` / `float` / `Decimal`、`bool` 是 `int` 的子类、`None` |
| A04 | [字符串、字节与编码](part-a/a04-strings-and-bytes.md) | `str` 与 `bytes`、编码、f-string |
| A05 | [运算符与表达式](part-a/a05-operators.md) | 地板除、短路、链式比较、增强赋值 |
| A06 | [控制流](part-a/a06-control-flow.md) | 分支、循环、`for`/`try` 的 `else` |
| A07 | [函数](part-a/a07-functions.md) | 定义、返回值、参数、文档字符串 |
| A08 | [列表、元组、字典、集合](part-a/a08-collections.md) | 四种容器的语义和典型坑 |
| A09 | [文件与路径](part-a/a09-files-and-paths.md) | `pathlib`、文本编码、`with` |
| A10 | [错误与异常](part-a/a10-exceptions.md) | 异常层次、`raise from`、不要裸 `except` |
| A11 | [模块、包与导入](part-a/a11-modules-and-packages.md) | `import`、`__name__`、包、循环导入 |
| A12 | [标准库入门地图](part-a/a12-stdlib-tour.md) | 知道去哪找，而不是重写一遍 |
| A13 | [小项目：成绩单](part-a/a13-gradebook.md) | 把 A 的内容合成一个小程序 |

### Part B　进阶

| 章 | 文件 | 你要掌握的 |
| --- | --- | --- |
| B01 | [参数、作用域与闭包](part-b/b01-scopes-and-closures.md) | LEGB、`nonlocal`、闭包迟绑定、`/` 与 `*` |
| B02 | [推导式与迭代协议](part-b/b02-iterables.md) | 可迭代、迭代器、`for` 实际在做什么 |
| B03 | [生成器](part-b/b03-generators.md) | `yield`、`yield from`、`close` / `throw` |
| B04 | [装饰器](part-b/b04-decorators.md) | 函数是对象、`functools.wraps`、叠加顺序 |
| B05 | [类与对象](part-b/b05-classes.md) | 类体、实例、继承、`super()` |
| B06 | [特殊方法与协议](part-b/b06-dunder-protocols.md) | 容器、可调用、比较；鸭子类型的边界 |
| B07 | [dataclass 与枚举](part-b/b07-dataclass-enum.md) | 何时用数据类，`Enum` 的身份语义 |
| B08 | [上下文管理器](part-b/b08-context-managers.md) | `with`、`contextlib`、异常抑制 |
| B09 | [类型注解](part-b/b09-type-hints.md) | 注解不是运行时校验；3.12 与 3.14 的差别 |
| B10 | [模式匹配](part-b/b10-pattern-matching.md) | `match` 是结构匹配，不是 C 的 `switch` |
| B11 | [常用标准库进阶](part-b/b11-stdlib-advanced.md) | `collections`、`itertools`、`functools`、日期与正则 |
| B12 | [测试与打包入门](part-b/b12-testing-packaging.md) | `unittest`、虚拟环境、`pyproject.toml` 长什么样 |
| B13 | [小项目：库存流水](part-b/b13-inventory.md) | 用类、枚举和测试写一个小领域模型 |

### Part C　语言、运行时、并发与性能

| 章 | 文件 | 你要掌握的 |
| --- | --- | --- |
| C01 | [执行模型与对象](part-c/c01-execution-and-objects.md) | 代码对象、帧、`PyObject` 头在概念上是什么 |
| C02 | [可变性、拷贝与身份](part-c/c02-mutability-copy-identity.md) | `is`、浅拷贝、深拷贝、驻留的真实边界 |
| C03 | [引用计数与垃圾回收](part-c/c03-gc.md) | 主路径是引用计数，循环才靠分代 GC |
| C04 | [字节码与解释器](part-c/c04-bytecode.md) | `dis`、自适应特化、为什么不要背 opcode |
| C05 | [GIL、线程与进程](part-c/c05-gil-threads-processes.md) | 锁保护什么、三种并发分别解决什么 |
| C06 | [asyncio](part-c/c06-asyncio.md) | 协作式调度、`TaskGroup`、取消 |
| C07 | [自由线程、子解释器与 3.13–3.15](part-c/c07-runtime-2026.md) | 把新版本放在一张准确的地图上 |
| C08 | [描述符、MRO 与元类](part-c/c08-descriptors-mro-metaclasses.md) | 属性查找顺序、C3、少写元类 |
| C09 | [测量与性能](part-c/c09-performance.md) | 先测量；复杂度；哪些微优化值得知道 |
| C10 | [深挖对照实验](part-c/c10-lab.md) | 一组把 C 部结论钉死的小实验 |

### Part D　工程与系统设计

| 章 | 文件 | 你要掌握的 |
| --- | --- | --- |
| D01 | [项目布局与依赖](part-d/d01-project-layout.md) | 源码布局、锁文件、可重复安装 |
| D02 | [测试策略](part-d/d02-testing-strategy.md) | 测行为、替身、不要靠睡眠制造时间 |
| D03 | [边界上的类型与校验](part-d/d03-boundaries.md) | 注解、`Protocol`、运行时校验各管一层 |
| D04 | [日志、配置与错误](part-d/d04-logging-config-errors.md) | 12-factor 配置、日志里不放密钥 |
| D05 | [HTTP API](part-d/d05-http-api.md) | 用标准库走通一个最小 HTTP 服务，并讲清 API 形状 |
| D06 | [持久化与事务](part-d/d06-persistence.md) | SQLite、参数化、事务 |
| D07 | [并发架构](part-d/d07-concurrency-architecture.md) | 队列、超时、取消、背压 |
| D08 | [安全基线](part-d/d08-security.md) | 参数化查询、路径约束、`compare_digest`、不反序列化不可信 pickle |
| D09 | [可观测性与关闭](part-d/d09-observability-shutdown.md) | 日志、请求号、SIGTERM 时把活干完 |
| D10 | [四个设计案例](part-d/d10-system-design.md) | 短链、限流、缓存、任务队列 |

### Part E　2026 面试题库

题库按主题拆开。每题包含考点、一种常见错法、一份可以直接说出口的回答，以及能跑的对照（集中在 `examples/part_e/`）。

| 文件 | 内容 |
| --- | --- |
| [E01 语言与语法](part-e/e01-language.md) | 类型、参数、容器、异常、导入 |
| [E02 数据模型](part-e/e02-data-model.md) | 对象、描述符、MRO、GC |
| [E03 并发与运行时](part-e/e03-concurrency.md) | GIL、线程、进程、asyncio、3.13–3.15 |
| [E04 性能](part-e/e04-performance.md) | 测量、复杂度、容器选型 |
| [E05 工程实践](part-e/e05-engineering.md) | 测试、配置、日志、安全、发布 |
| [E06 系统设计](part-e/e06-system-design.md) | 短链、限流、缓存、队列、一致性 |
| [E07 手写小题](part-e/e07-coding-drills.md) | 限流器、LRU、重试、分组、管道 |

## 目录怎么对应

```text
docs/python-tutorial/          教程正文
examples/part_a … part_e       可运行示例
examples/run_all.py            串行跑完所有示例
```

正文引用示例时使用仓库内路径，例如 `examples/part_a/a02_names_and_objects.py`。
