"""
现代控制流结构、for-else 协议与模式匹配。
展示：for-else 优雅搜索、卫语句 (Guard Clause)、match-case 结构化分发。
"""

from typing import Any


def search_healthy_node(nodes: list[dict[str, Any]]) -> str:
    """使用 for-else 消除 flag 变量，探测可用集群节点。"""
    for node in nodes:
        if node.get("status") == "healthy" and node.get("latency_ms", 999) < 50:
            print(f"[Discovery] 命中健康低延迟节点: {node['host']}")
            return str(node["host"])
    else:
        # 仅在无 break 正常遍历结束后触发
        print("[Discovery Fallback] 未发现合格节点，切换为备用容灾集群")
        return "fallback.cluster.internal"


def process_packet(packet: dict[str, Any]) -> str:
    """演示 Python 3.10+ match-case 模式匹配与结构化解构。"""
    match packet:
        case {"type": "heartbeat", "seq": int(seq)}:
            return f"ACK: heartbeat {seq}"
        case {"type": "data", "payload": str(data)} if len(data) > 0:
            return f"PROCESSED: {len(data)} bytes"
        case _:
            return "DROPPED: invalid packet"


def main() -> None:
    print("=== 03. 控制流与高级循环结构 ===")
    mock_nodes = [
        {"host": "node-01", "status": "unhealthy", "latency_ms": 120},
        {"host": "node-02", "status": "healthy", "latency_ms": 25},
    ]
    healthy_host = search_healthy_node(mock_nodes)
    print(f"路由选择结果: {healthy_host}")

    # match-case 测试
    res1 = process_packet({"type": "heartbeat", "seq": 1001})
    res2 = process_packet({"type": "unknown"})
    print(f"[Match-Case] {res1} | {res2}")
    print("=== 演示完成 ===")


if __name__ == "__main__":
    main()
