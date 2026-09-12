# 阶段 02: 底层对象模型与内存机制

Python 之所以被称为“一切皆对象”，其底层基石全在于 CPython 的对象模型与内存管理系统。深入本阶段，将帮助工程师彻底打通从 Python 高层抽象到底层 C 结构体与 GC 垃圾回收的心智闭环。

---

## 💡 核心工程心智与底层机制

1. **PyObject 核心结构体**：
   - CPython 中所有对象在堆内存中均以 `PyObject` 或 `PyVarObject` 结构体呈现；
   - 核心字段包含 `ob_refcnt`（引用计数器，实现 $O(1)$ 即时内存回收）和 `ob_type`（指向类型对象的类型指针）。
2. **可变性（Mutability）与深浅拷贝**：
   - 不可变对象（int, str, tuple）修改必定创建新对象并重新绑定引用；
   - 浅拷贝（`copy.copy`）仅复制最外层容器指针，内部元素引用共享；生产复杂嵌套配置必须采用 `copy.deepcopy` 规避并发脏写。
3. **驻留机制（Interning）与小整数池**：
   - CPython 虚拟机在启动阶段即在静态内存区常驻了 `[-5, 256]` 的小整数池；
   - 采用字符串驻留机制（String Interning）优化编译期常量比对，大幅降低内存开销并加速字典 Hash 查找。
4. **分代垃圾回收与循环引用治理**：
   - 纯粹的引用计数无法处理“循环引用（Reference Cycles）”导致的内存泄漏；
   - CPython 通过分代收集（Generation 0/1/2）与双向链表三色标记清除算法作为兜底；生产高频对象环需利用 `weakref` 弱引用主动解耦。

---

## 🗺️ 阶段专题导航

| 专题目录 | 核心原语 | 关键掌握目标 |
| :--- | :--- | :--- |
| **[01-pyobject-and-memory-model](./01-pyobject-and-memory-model/)** | PyObject 结构与引用计数 | 深入 C 结构体模型、`sys.getrefcount` 探针与引用计数生灭生命周期 |
| **[02-mutability-and-deep-shallow-copy](./02-mutability-and-deep-shallow-copy/)** | 可变性机制与深浅拷贝 | 掌握深浅拷贝物理指针拓扑、内存逃逸与嵌套结构并发安全性 |
| **[03-interning-and-identity](./03-interning-and-identity/)** | 小整数池与字符串驻留 | 掌握 `[-5, 256]` 预分配机制、常量编译驻留与 `is` 底层优化原理 |
| **[04-garbage-collection-and-gc](./04-garbage-collection-and-gc/)** | 三代 GC 回收与循环引用 | 掌握分代收集阈值、三色标记与 `weakref` 生产级内存防泄漏设计 |

---

## 🚀 统一运行验证

```bash
uv run python 02-python-data-model-and-memory/01-pyobject-and-memory-model/main.py
uv run python 02-python-data-model-and-memory/02-mutability-and-deep-shallow-copy/main.py
uv run python 02-python-data-model-and-memory/03-interning-and-identity/main.py
uv run python 02-python-data-model-and-memory/04-garbage-collection-and-gc/main.py
```
