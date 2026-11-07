# A12　标准库入门地图

> 示例：`examples/part_a/a12_stdlib.py`

## 学完你能做什么

遇到常见任务时先去标准库，而不是抄一段来源不清的代码。这一章不是把标准库讲完，那会比整本教程还长。

## 怎么查

官方文档的库参考按模块索引。你本机的版本用 `python -m pydoc json` 或交互式 `help(json)` 查看，避免看错到 3.15 才有的函数然后在 3.12 上调用。

本教程后面会用到、现在先认识的模块：

| 模块 | 用来做什么 | 不要用来做什么 |
| --- | --- | --- |
| `json` | 读写 JSON 文本 | 当配置语言的全部（想要注释和更安全的类型时，TOML 用 3.11 就有的 `tomllib` 读） |
| `pathlib` | 路径 | 手工拼分隔符 |
| `datetime` | 时刻和日历 | 用朴素 datetime 表示“这个瞬间”还不带时区 |
| `math` | 浮点数学 | 精确十进制，那是 `decimal` |
| `statistics` | 均值、中位数 | 代替专业统计推断库 |
| `random` | 模拟、洗牌 | 生成密码、令牌。密码学用 `secrets` |
| `argparse` | 命令行参数 | 在库模块顶层解析 `sys.argv` |

## JSON

`json.loads` 把文本变成 Python 对象：对象变成 `dict`，数组变成 `list`，`null` 变成 `None`。`json.dumps` 反向走。字典的键会变成字符串。不是 JSON 能表示的对象，例如集合、字节、自定义类，需要你自己转换，否则 `TypeError`。

示例里 `sort_keys=True` 是为了断言稳定，不是业务必需。JSON 对象的规范并不关心键顺序；Python 读回来的 `dict` 会保留文本里的顺序。

## 时间

```python
from datetime import UTC, datetime

moment = datetime(2026, 11, 7, tzinfo=UTC)
```

`UTC` 是 3.11 加入 `datetime` 的常量。带 `tzinfo` 的叫 aware，不带的叫 naive。一个表示“事件发生瞬间”的值应该是 aware。只表示“墙上的年月日”可以是 `date`，不必强行变成时刻。

不要用 `datetime.utcnow()`，它产生的是 naive 对象，3.12 已经把它标为弃用。用 `datetime.now(UTC)`。

## 随机

`random.Random(0)` 得到一个独立的生成器，种子固定，测试就可以断言序列。不要用全局的 `random.seed` 影响整个进程，别的库可能也在用它。

示例比较两个同一种子的生成器，序列一致。没有种子的 `random` 不适合放进断言。

## 你现在不必装的东西

HTTP 客户端、数据库驱动、类型校验、Web 框架都有成熟的第三方库。A 阶段用标准库把语言写正确。D05 用标准库的 `http.server` 演示一个最小 HTTP 服务，是为了不把“听懂请求和响应”绑在某一个框架的教程上。真要做服务，再选框架，并单独学那个框架的生命周期。本仓库 `08-modern-web-frameworks` 里有 FastAPI 的专题，那是另一条材料，不是本章的依赖。

## 常见错误

- 用 `random` 生成会话令牌。用 `secrets.token_urlsafe`。
- `json.loads` 的输入其实是字节，编码还不确定。先按字节来源解码，或者在你知道它是 UTF-8 时再解码。`json.loads` 也接受 UTF-8 字节，但来源不明的二进制不该直接送进去。
- 把本地时间当成 UTC 存进数据库，以后换一台机器就对不上。

## 练习

1. 把 `{"ok": true}` 解析成 Python，并取出布尔值。注意 JSON 的 `true` 会变成 Python 的 `True`。
2. 用种子 `1` 构造 `random.Random`，取两次 `randrange(100)`，再新建一个同样种子的生成器取两次，断言相等。
3. 说出一个不该用 `random` 的场景。

参考答案：

1. `json.loads('{"ok": true}')["ok"] is True`。
2. 两个 `random.Random(1)` 各自取两次，列表相等。不要交叉使用同一个生成器还期待和“新生成器的前两次”以外的序列相同。
3. 密码、重置链接、API 密钥、任何攻击者能预测就有后果的值。

## 小结

标准库覆盖了文本、路径、时间和受控的随机数。查文档时对准 3.12。安全相关的随机数、时区、编码这三件事从一开始就用对的 API，后面就不用返工。
