# 03-control-flow-statements: 控制流与循环高级特性

## 一、核心机制与设计哲学

- **结构化控制流**：Python 提供 `if-elif-else` 分支，以及 `for-in` 与 `while` 迭代循环。Python 的 `for` 循环本质是**基于迭代器协议（`iter()` 和 `next()`）**的高阶封装，而非 C 风格基于计数器的指针游标。
- **独创语法：`for...else` 与 `while...else`**：
  - `else` 子句紧跟在循环块之后。
  - **触发条件**：只有当循环**自然耗尽迭代器（正常结束）**时，`else` 块才会执行；如果循环是通过 `break` 语句主动跳出，则 `else` 块被**跳过**。
  - **设计初衷**：消除在搜索算法中设置“flag 布尔标记变量”（如 `found = False`）的冗余样板代码。

## 二、生产规范与避坑指南

1. **扁平化结构与卫语句（Guard Clauses）**：严禁深层嵌套 `if-else`（超过 3 层）。应优先使用卫语句提前 `return` 或 `continue`，降低代码认知圈复杂度。
2. **遍历中就地修改容器陷阱**：严禁在直接遍历列表的同时调用 `list.remove()` 或 `del`，这会导致迭代器内部索引偏移引起“漏删”Bug。生产中应采用列表推导式生成新列表，或逆序遍历。
3. **现代模式匹配（Structural Pattern Matching）**：Python 3.10+ 引入 `match-case`，支持解构匹配字典、对象属性与类型守卫，全面替代冗长的 `if-isinstance-getattr` 链。

## 三、典型工程示例解析

查看同目录下 `main.py`：
- 演示了在服务发现/连接重试场景下，利用 `for...else` 优雅实现探测与降级；
- 演示了卫语句解构复杂业务逻辑；
- 演示了 Python 3.10+ `match...case` 的结构化解构。
