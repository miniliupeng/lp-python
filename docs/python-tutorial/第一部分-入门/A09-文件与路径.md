# A09　文件与路径

> 示例：`examples/part_a/a09_files.py`

## 学完你能做什么

用 `pathlib` 定位文件，用 `with` 保证关闭，并用 UTF-8 读写文本。不在字符串上手工拼接路径。

## 路径是对象

`pathlib.Path` 表示一条路径。`/` 运算符拼接片段，会按当前系统处理分隔符：

```python
path = root / "notes" / "hello.txt"
```

常用属性：`name`（文件名）、`suffix`（扩展名，带点）、`parent`、`stem`（去掉扩展名）。`relative_to` 求相对路径，前提是它确实在那个目录之下，否则抛 `ValueError`。

`mkdir(parents=True, exist_ok=True)` 用来创建目录。示例里父目录确定不存在，所以只调用了一次 `mkdir()`。已经可能存在时加上 `exist_ok=True`，避免和别的进程互相撞出 `FileExistsError`。

遍历目录用 `iterdir()`。它不是递归的。3.12 的 `Path.walk()` 才提供类似 `os.walk` 的递归遍历。示例只用了一层。

## 文本要写编码

```python
path.write_text("你好\n第二行\n", encoding="utf-8")
path.read_text(encoding="utf-8").splitlines()
```

`splitlines()` 按行切开并去掉行尾，平台的 `\n` 和 `\r\n` 都覆盖。不要用 `split("\n")` 处理来自 Windows 的文件，除非你确定内容里只有 `\n`。

更细的控制用 `with path.open("r", encoding="utf-8") as handle:`。`with` 离开代码块时关闭文件，包括块里发生异常的情况。A10 和 B08 解释它背后的协议。现在先当成“申请资源，用完一定还”的语法。

二进制用 `"rb"` / `"wb"`，这时没有文本编码，读写的是 `bytes`。图片、压缩包、任何不是文本的格式都走二进制。不要先当文本读进来再 `encode` 回去。

## 临时文件

示例用 `tempfile.TemporaryDirectory()`。离开 `with` 后目录被删掉，测试不会在仓库里留下 `note.txt`。库代码如果需要持久文件，路径应该由调用方传入，不要写死到家目录或当前目录。

当前工作目录取决于你在哪里启动进程，不是取决于 `.py` 文件放在哪。脚本旁边的数据文件用 `Path(__file__).resolve().parent` 定位，不要假设用户正好在那个目录里执行。

## 常见错误

- 用 `"../" + name` 拼接用户输入。这既不跨平台，也会在 D08 变成路径穿越问题。
- 打开文件后不关闭。小脚本有时能靠进程退出混过去，库代码不行。用 `with`。
- 省略 `encoding`。3.12 跟区域设置走，3.15 默认 UTF-8。显式写出，两边都正确。

## 练习

1. 给定 `Path("/tmp/a/b.txt")`，`name`、`suffix`、`parent` 各是什么？在你自己的机器上用绝对路径试，不要假设盘符。
2. 写一段代码，把三行文字写到临时文件再读出来，行列表应当和写入前一致。
3. 为什么示例可以在断言之后不再调用 `unlink`？

参考答案：

1. `name` 是 `b.txt`，`suffix` 是 `.txt`，`parent` 是 `/tmp/a`。Windows 上根不一样，但这三个属性的含义相同。
2. 结构就是示例里的 `write_text` / `read_text` / `splitlines`。
3. `TemporaryDirectory` 的 `__exit__` 会删除整个目录，文件一起消失。

## 小结

路径用 `Path` 拼接和查询。文本读写显式 UTF-8。资源用 `with` 关闭。不要依赖进程的当前目录去找包在仓库里的文件。
