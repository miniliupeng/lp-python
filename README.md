# Python 全景教程：从零基础到 2026 面试

这是一份从零写起的中文教程。读者可以没有编程背景。读完第一部分能写小脚本；读完第二部分能读懂日常业务代码；第三部分解释 CPython 怎么执行这些代码；第四部分把语言放到服务和系统设计里；第五部分是对照答案用的题库。

这个分支只有这份教程，不包含其他专题目录。

正文在 [`docs/python-tutorial/`](docs/python-tutorial/README.md)。可运行示例在 [`examples/`](examples/run_all.py)。

## 版本

可执行示例锁定 **CPython 3.12**，已在 **3.12.3** 上跑通。语法和标准库调用都不使用 3.13 及以上才有的形式。

语言叙述以 Python 3.12 为基准。3.13（2024-10）、3.14（2025-10-07）、3.15（2026-10-09，写作时文档站可见 3.15.2）只在标明版本的段落里出现。默认说的是 CPython，不是 PyPy。

2026 年 11 月需要先记住的三句：

- 默认的 CPython 构建仍然有 GIL。自由线程是 3.14 起官方支持的可选构建，不是默认解释器。
- JIT 到 3.15 仍是实验特性，默认不打开。
- 3.14 才有 t-string、默认延迟注解和 `concurrent.interpreters`。3.15 才有 `lazy` 导入和内置 `frozendict`（它不是 `dict` 的子类）。

语言保证和 CPython 实现细节在教程里分开写。比较数字用 `==`。`-5` 到 `256` 的整数缓存只是 CPython 的实现。

## 怎么读

1. 每一章先跑对应示例，再读正文。示例用断言固定行为。
2. 零基础按第一部分 → 第二部分 → 第三部分 → 第四部分的顺序读。
3. 有其他语言经验：先读 A02、A05、A08，然后从第二部分读到第四部分。
4. 准备面试：第三部分、第四部分读完再做第五部分。先写出自己的答案，再对照。题库里的“常见错法”不要背。

```bash
python examples/run_all.py
```

只跑一章时，执行该章给出的文件，例如：

```bash
python examples/part_a/a02_names_and_objects.py
```

示例只依赖标准库。

## 大纲

章节目录和 Markdown 文件名用中文。示例代码仍在 `examples/part_a` 到 `examples/part_e`，文件名保持英文。

### 第一部分　入门

1. [A01-安装运行与执行](docs/python-tutorial/第一部分-入门/A01-安装运行与执行.md) — 安装、运行，以及 Python 到底在执行什么
2. [A02-名字对象与类型](docs/python-tutorial/第一部分-入门/A02-名字对象与类型.md) — 名字、对象、动态强类型
3. [A03-数字布尔与None](docs/python-tutorial/第一部分-入门/A03-数字布尔与None.md) — 数字、布尔、None
4. [A04-字符串字节与编码](docs/python-tutorial/第一部分-入门/A04-字符串字节与编码.md) — 字符串、字节与编码
5. [A05-运算符与表达式](docs/python-tutorial/第一部分-入门/A05-运算符与表达式.md) — 运算符与表达式
6. [A06-控制流](docs/python-tutorial/第一部分-入门/A06-控制流.md) — 控制流
7. [A07-函数](docs/python-tutorial/第一部分-入门/A07-函数.md) — 函数
8. [A08-列表元组字典集合](docs/python-tutorial/第一部分-入门/A08-列表元组字典集合.md) — 列表、元组、字典、集合
9. [A09-文件与路径](docs/python-tutorial/第一部分-入门/A09-文件与路径.md) — 文件与路径
10. [A10-错误与异常](docs/python-tutorial/第一部分-入门/A10-错误与异常.md) — 错误与异常
11. [A11-模块包与导入](docs/python-tutorial/第一部分-入门/A11-模块包与导入.md) — 模块、包与导入
12. [A12-标准库入门](docs/python-tutorial/第一部分-入门/A12-标准库入门.md) — 标准库入门地图
13. [A13-成绩单](docs/python-tutorial/第一部分-入门/A13-成绩单.md) — 小项目：成绩单

### 第二部分　进阶

1. [B01-作用域与闭包](docs/python-tutorial/第二部分-进阶/B01-作用域与闭包.md) — 参数、作用域与闭包
2. [B02-推导式与迭代](docs/python-tutorial/第二部分-进阶/B02-推导式与迭代.md) — 推导式与迭代协议
3. [B03-生成器](docs/python-tutorial/第二部分-进阶/B03-生成器.md) — 生成器
4. [B04-装饰器](docs/python-tutorial/第二部分-进阶/B04-装饰器.md) — 装饰器
5. [B05-类与对象](docs/python-tutorial/第二部分-进阶/B05-类与对象.md) — 类与对象
6. [B06-特殊方法与协议](docs/python-tutorial/第二部分-进阶/B06-特殊方法与协议.md) — 特殊方法与协议
7. [B07-数据类与枚举](docs/python-tutorial/第二部分-进阶/B07-数据类与枚举.md) — dataclass 与枚举
8. [B08-上下文管理器](docs/python-tutorial/第二部分-进阶/B08-上下文管理器.md) — 上下文管理器
9. [B09-类型注解](docs/python-tutorial/第二部分-进阶/B09-类型注解.md) — 类型注解
10. [B10-模式匹配](docs/python-tutorial/第二部分-进阶/B10-模式匹配.md) — 模式匹配
11. [B11-标准库进阶](docs/python-tutorial/第二部分-进阶/B11-标准库进阶.md) — 常用标准库进阶
12. [B12-测试与打包](docs/python-tutorial/第二部分-进阶/B12-测试与打包.md) — 测试与打包入门
13. [B13-库存流水](docs/python-tutorial/第二部分-进阶/B13-库存流水.md) — 小项目：库存流水

### 第三部分　语言、运行时、并发与性能

1. [C01-执行模型与对象](docs/python-tutorial/第三部分-运行时/C01-执行模型与对象.md) — 执行模型与对象
2. [C02-可变性拷贝与身份](docs/python-tutorial/第三部分-运行时/C02-可变性拷贝与身份.md) — 可变性、拷贝与身份
3. [C03-引用计数与垃圾回收](docs/python-tutorial/第三部分-运行时/C03-引用计数与垃圾回收.md) — 引用计数与垃圾回收
4. [C04-字节码与解释器](docs/python-tutorial/第三部分-运行时/C04-字节码与解释器.md) — 字节码与解释器
5. [C05-GIL线程与进程](docs/python-tutorial/第三部分-运行时/C05-GIL线程与进程.md) — GIL、线程与进程
6. [C06-协程与asyncio](docs/python-tutorial/第三部分-运行时/C06-协程与asyncio.md) — asyncio
7. [C07-自由线程与新版本](docs/python-tutorial/第三部分-运行时/C07-自由线程与新版本.md) — 自由线程、子解释器与 3.13–3.15
8. [C08-描述符MRO与元类](docs/python-tutorial/第三部分-运行时/C08-描述符MRO与元类.md) — 描述符、MRO 与元类
9. [C09-测量与性能](docs/python-tutorial/第三部分-运行时/C09-测量与性能.md) — 测量与性能
10. [C10-对照实验](docs/python-tutorial/第三部分-运行时/C10-对照实验.md) — 深挖对照实验

### 第四部分　工程与系统设计

1. [D01-项目布局与依赖](docs/python-tutorial/第四部分-工程/D01-项目布局与依赖.md) — 项目布局与依赖声明
2. [D02-测试策略](docs/python-tutorial/第四部分-工程/D02-测试策略.md) — 测试策略
3. [D03-边界上的类型与校验](docs/python-tutorial/第四部分-工程/D03-边界上的类型与校验.md) — 边界上的类型与校验
4. [D04-日志配置与错误](docs/python-tutorial/第四部分-工程/D04-日志配置与错误.md) — 日志、配置与错误
5. [D05-HTTP接口](docs/python-tutorial/第四部分-工程/D05-HTTP接口.md) — HTTP API
6. [D06-持久化与事务](docs/python-tutorial/第四部分-工程/D06-持久化与事务.md) — 持久化与事务
7. [D07-并发架构](docs/python-tutorial/第四部分-工程/D07-并发架构.md) — 并发架构：队列、超时、取消、背压
8. [D08-安全基线](docs/python-tutorial/第四部分-工程/D08-安全基线.md) — 安全基线
9. [D09-可观测性与关闭](docs/python-tutorial/第四部分-工程/D09-可观测性与关闭.md) — 可观测性与进程关闭
10. [D10-设计案例](docs/python-tutorial/第四部分-工程/D10-设计案例.md) — 设计案例：短链、限流、缓存、任务队列

### 第五部分　2026 面试题库

1. [E01-语言与语法](docs/python-tutorial/第五部分-面试/E01-语言与语法.md) — 语言与语法
2. [E02-数据模型](docs/python-tutorial/第五部分-面试/E02-数据模型.md) — 数据模型
3. [E03-并发与运行时](docs/python-tutorial/第五部分-面试/E03-并发与运行时.md) — 并发与运行时
4. [E04-性能](docs/python-tutorial/第五部分-面试/E04-性能.md) — 性能
5. [E05-工程实践](docs/python-tutorial/第五部分-面试/E05-工程实践.md) — 工程实践
6. [E06-系统设计](docs/python-tutorial/第五部分-面试/E06-系统设计.md) — 系统设计
7. [E07-手写小题](docs/python-tutorial/第五部分-面试/E07-手写小题.md) — 手写小题

每章的掌握点和示例路径见 [`docs/python-tutorial/README.md`](docs/python-tutorial/README.md)。
