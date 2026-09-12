# 专题 01：异步 SQLite 操作、预编译语句（Prepared Statements）与 WAL 模式

在微服务单体化（Modular Monolith）、边缘计算与本地轻量数据存储中，**SQLite** 是最广泛部署的数据库。而在高并发异步架构中，传统同步 `sqlite3` 驱动会直接阻塞主事件循环。通过 **`aiosqlite`** 配合 **预编译参数化语句（Prepared Statements）** 与 **WAL（Write-Ahead Logging）模式**，可以实现高并发读写与 100% 免疫 SQL 注入攻击的工业级底座。

---

## 一、 痛点驱动：SQL 注入灾难与同步阻塞雪崩

1. **SQL 注入漏洞（SQL Injection）**：
   - 开发者使用字符串拼接（f-string）构造 SQL：`f"SELECT * FROM users WHERE name = '{input}'"`；
   - 攻击者输入 `admin' OR '1'='1`，直接篡改了 SQL 的 AST 语法树结构，导致全量机密数据拖库甚至删库；
2. **SQLite 默认日志模式的写阻塞读**：
   - 默认回滚日志（Rollback Journal）在执行写事务时必须独占排他锁，导致全站所有读取操作全部被阻塞超时挂起。

---

## 二、 机制解密：预编译参数化原理与 WAL 读写分离

```text
[ SQL 注入 vs 预编译参数化 ]
  恶意输入: "admin' OR 1=1 --"

  f-string 拼接 ──> 送入数据库语法解析器 ──> 结构被破坏篡改！OR 1=1 变成逻辑分支！
  预编译语句 (?) ─> 预先编译固定语法树结构 ─> 参数只作为纯字符串标量传入 (绝不可能改变语法树结构！)

[ WAL (Write-Ahead Logging) 并发革命 ]
  写入事务 ──> 顺序追加写入独立 wal 文件 (极速，单文件追加)
  读取事务 ──> 直接读取主 db 文件 + 内存 wal 索引 (读写完全互不阻塞并发执行！)
```

1. **预编译在内核 AST 层的免疫机制**：
   - 数据库引擎先对包含占位符 `?` 的 SQL 模板进行词法分析与语法树（AST）编译生成执行计划；
   - 随后传入的参数无论包含多少单引号或 SQL 关键字，都只被严格当作**不可执行的纯文本字面量（Literal Value）**填充，从数学上彻底根除了注入可能；
2. **开启 WAL 模式**：
   - 执行 `PRAGMA journal_mode=WAL;` 彻底解锁读写并发能力。

---

## 三、 生产规范与最佳实践

- **零容忍任何 SQL 字符串拼接**：所有动态入参必须无条件通过参数元组传递（如 `cursor.execute(sql, (param,))`）；
- **连接关闭保障**：必须使用 `async with aiosqlite.connect(...) as db:` 确保连接与事务被确定性析构。
