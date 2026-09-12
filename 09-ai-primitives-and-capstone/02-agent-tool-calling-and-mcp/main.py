"""专题 02: AI Agent 函数调用 (Tool Calling) 调度器与协议分发."""

import json
from collections.abc import Callable
from typing import Any


class ToolRegistry:
    """标准函数调用与协议分发注册中心."""

    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {}
        self.schemas: list[dict[str, Any]] = []

    def register(
        self, name: str, desc: str, params: dict[str, Any], fn: Callable[..., Any]
    ) -> None:
        self._tools[name] = fn
        self.schemas.append(
            {
                "type": "function",
                "function": {"name": name, "description": desc, "parameters": params},
            }
        )

    def dispatch(self, tool_name: str, args_json: str) -> dict[str, Any]:
        if tool_name not in self._tools:
            return {"status": "error", "error": f"未注册工具: {tool_name}"}
        try:
            args = json.loads(args_json)
            return {"status": "success", "result": self._tools[tool_name](**args)}
        except Exception as exc:
            return {"status": "error", "error": str(exc)}


def query_system_metric(metric_name: str, server_id: str) -> dict[str, Any]:
    """模拟查询系统指标的工具函数."""
    return {"server": server_id, "metric": metric_name, "value": "98.5%"}


def main() -> None:
    print("=== [08-02] AI Agent Tool Calling 与协议分发实操 ===")
    registry = ToolRegistry()

    # 1. 注册工具及其标准 JSON Schema
    registry.register(
        name="query_system_metric",
        desc="查询指定服务器关键指标",
        params={
            "type": "object",
            "properties": {
                "metric_name": {"type": "string"},
                "server_id": {"type": "string"},
            },
            "required": ["metric_name", "server_id"],
        },
        fn=query_system_metric,
    )

    # 2. 模拟大模型输出的 ToolCall 指令并执行物理分发
    mock_call = {
        "name": "query_system_metric",
        "arguments": '{"metric_name": "cpu", "server_id": "node-01"}',
    }
    print("  • 大模型输出工具调用指令:", mock_call)

    execution_res = registry.dispatch(mock_call["name"], mock_call["arguments"])
    print("  • 物理执行产出 ToolResult:", execution_res)

    assert execution_res["status"] == "success"
    assert execution_res["result"]["server"] == "node-01"
    print("✅ Tool Calling 契约解析与分发执行闭环验证通过。")


if __name__ == "__main__":
    main()
