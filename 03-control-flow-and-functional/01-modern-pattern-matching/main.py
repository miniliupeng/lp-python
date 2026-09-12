"""专题 01: 现代结构化模式匹配 (match-case) 与解构分发

演示在事件网关处理中使用 match-case 实现字典结构解构、
类模式匹配、守卫条件拦截与通配符兜底处理。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class OrderEvent:
    order_id: str
    amount: float
    user_tier: str


def dispatch_event(event: object) -> str:
    """基于结构化模式匹配的事件统一安全分发器."""
    match event:
        # 1. 强类型类模式解构 + 守卫条件 (Guard)
        case OrderEvent(order_id=oid, amount=amt, user_tier="vip") if amt >= 1000:
            return f"VIP 大额订单审批: {oid}, 金额: {amt}"

        case OrderEvent(order_id=oid, amount=amt):
            return f"普通订单正常流转: {oid}, 金额: {amt}"

        # 2. 异构字典结构解构
        case {"type": "ping", "timestamp": ts}:
            return f"健康检查心跳包: ts={ts}"

        case {"type": "alert", "level": "critical", "msg": str(message)}:
            return f"🚨 严重系统告警: {message}"

        # 3. 通配符兜底 (防止未捕获事件穿透)
        case _:
            return "未知事件协议，安全降级丢弃"


def main() -> None:
    print("=== [02-01] 现代结构化模式匹配 (match-case) 实操 ===")

    events = [
        OrderEvent("ORD-001", 12000.0, "vip"),
        OrderEvent("ORD-002", 88.0, "regular"),
        {"type": "ping", "timestamp": 1726123456},
        {"type": "alert", "level": "critical", "msg": "数据库只读锁已触发"},
        "invalid_raw_string",
    ]

    for ev in events:
        result = dispatch_event(ev)
        print(f"  • 处理结果: {result}")

    print("✅ 结构化模式匹配分发验证通过，消除深层条件嵌套。")


if __name__ == "__main__":
    main()
