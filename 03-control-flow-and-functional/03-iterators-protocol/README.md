# 专题 03：迭代器协议（__iter__ 与 __next__）与流式分页容器设计

在 Python 的数据抽象中，**迭代协议（Iteration Protocol）**是整个语言控制流与容器遍历的基石。无论是 `for` 循环、列表推导式、解包赋值还是 `zip`/`enumerate`，底层都完全依赖统一的迭代器协议。掌握自定义迭代器与流式消费，是避免海量数据导致内存耗尽（OOM）的基本功。

---

## 一、 痛点驱动：全量加载海量数据的内存溢出（OOM）

从外部数据库、分页 API 或超大文件中读取百万级记录时：
```python
def get_all_records():
    records = []
    while has_next():
        records.extend(
            fetch_page()
        )  # ❌ 瞬间撑爆数十 GB 内存导致进程被 OS OOM-Killer 杀死
    return records
```
传统全量将数据加载到内存列表的方式在海量数据流面前极其脆弱。系统需要一种**按需拉取、恒定 O(1) 内存消耗**的流式抽象协议。

---

## 二、 机制解密：可迭代对象与迭代器的双方法契约

```text
[ 可迭代对象 (Iterable) ]
  必须实现 __iter__() ──> 返回一个崭新的迭代器实例 (Iterator)

[ 迭代器实例 (Iterator) ]
  ├── 必须实现 __iter__() ──> 恒定返回 self 自身
  └── 必须实现 __next__() ──> 依次返回下一个值，无数据时抛出 StopIteration 终止信号
```

1. **for 循环的底层等价展开**：
   ```python
   # for item in iterable 的底层真实执行流
   iterator = iter(iterable)  # 底层触发 iterable.__iter__()
   while True:
       try:
           item = next(iterator)  # 底层触发 iterator.__next__()
           # 执行循环体
       except StopIteration:
           break  # 安全静默捕获并退出
   ```
2. **一次性消费原则（Exhaustible）**：
   - 迭代器内部维护游标状态。一旦遍历完成，后续调用 `next()` 永远只抛出 `StopIteration`；若需再次遍历，必须通过可迭代对象重新获取一个新的迭代器。

---

## 三、 生产规范与避坑指南

- **自定义迭代器必须自身也是可迭代的**：即迭代器的 `__iter__` 必须 `return self`；
- **利用 `StopIteration` 干净终止**：禁止在迭代器内部返回特殊的魔法哨兵值来表示结束，标准异常终止是 Pythonic 的核心契约。
