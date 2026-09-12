"""专题 01: 对象构造阶段 (__new__) 与初始化阶段 (__init__) 分离

演示对象的生命周期流转、执行先后时序，
以及如何利用 __new__ 实现一个企业级线程安全的单例模式 (Singleton)。
"""

import threading


class ThreadSafeSingleton:
    """利用 __new__ 与互斥锁实现的线程安全单例基类."""

    _instance: "ThreadSafeSingleton | None" = None
    _lock: threading.Lock = threading.Lock()
    _is_initialized: bool = False

    def __new__(cls, *args: object, **kwargs: object) -> "ThreadSafeSingleton":
        # 双重检查锁定 (Double-Checked Locking)
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    # 真正向底层堆分配内存物理对象
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, service_name: str = "default") -> None:
        # 防止单例模式每次调用 Class() 时重复执行初始化
        if not self._is_initialized:
            with self._lock:
                if not self._is_initialized:
                    self.service_name = service_name
                    self._is_initialized = True


def main() -> None:
    print("=== [03-01] 对象生命周期 (__new__ vs __init__) 与单例 ===")

    # 1. 多次实例化单例
    client_a = ThreadSafeSingleton("PaymentService")
    client_b = ThreadSafeSingleton("OrderService")

    print(f"  • client_a 服务名: {client_a.service_name}")
    print(f"  • client_b 服务名: {client_b.service_name} (保持初始值，未被二次覆写)")
    print(f"  • client_a 与 client_b 物理同一性: {client_a is client_b}")

    assert client_a is client_b, "单例模式多次调用必须返回同一物理对象"
    assert client_b.service_name == "PaymentService", "初始化逻辑必须具备幂等性"

    print("✅ __new__ 控制对象物理分配与单例保障验证通过。")


if __name__ == "__main__":
    main()
