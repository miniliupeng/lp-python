# 专题 04：生成器状态机、yield 惰性求值与 send() 双向通信

如果说迭代器是数据流消费的规范，那么**生成器（Generators）**就是 Python 实现**协作式多任务与惰性求值（Lazy Evaluation）**的底层神器。通过 `yield` 关键字，Python 函数从传统的“单次执行、返回销毁”转变为“状态保留、多次挂起唤醒”的有状态协程原语，更是早起 `asyncio` 发展史的演进母体。

---

## 一、 痛点驱动：列表推导式的瞬时内存暴涨

当需要对一个 1000 万行的日志文件进行清洗与过滤时：
```python
# ❌ 内存瞬间暴涨数 GB，导致容器被 Kubernetes 驱逐
clean_lines = [line.strip().upper() for line in open("huge.log")]
```
列表推导式在求值瞬间必须在堆上为数千万个元素全部分配内存。而系统真正需要的，是“**消费一个、计算一个、交付一个**”的惰性流式计算流水线。

---

## 二、 机制解密：生成器帧对象（Frame Object）与四大生命周期

```text
生成器函数调用 ──> 创建 PyGenObject (不执行任何函数体代码)
                      ├── 绑定当前执行栈帧 (PyFrameObject)
                      └── 初始状态: GEN_CREATED

调用 next(gen) / gen.send(val):
  GEN_SUSPENDED (挂起) ──[唤醒执行至下一个 yield]──> GEN_SUSPENDED (再次挂起并返回输出)
        │
        └─[执行完毕退出]──> GEN_CLOSED (抛出 StopIteration 携带 return 返回值)
```

1. **栈帧保留（Stack Frame Preservation）**：
   - 普通函数执行返回后，其局部调用栈帧立即被销毁回收；
   - 生成器函数遇到 `yield` 时，CPython 将其执行指令指针（`f_lasti`）与当前局部变量表**原样冻结在堆上的帧对象中**，直接出让 CPU 控制权；
2. **`send()` 实现双向管道通信**：
   - `yield` 不仅是一个输出操作，它还是一个**表达式**！调用方通过 `gen.send(value)` 可以将外部的新指令动态注入给正在运行中的生成器内部，实现双向互动。

---

## 三、 生产规范与最佳实践

- **构建流式处理管道（Pipelines）**：将生成器按单一职责串联（读取 $	o$ 解析 $	o$ 过滤 $	o$ 存储），全链路保持极低内存占用；
- **利用 `yield from` 委托子生成器**：高效透传双向异常与返回值，规避手动写循环转发。
