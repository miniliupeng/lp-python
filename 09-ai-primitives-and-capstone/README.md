# 阶段 09: AI 原语、智能体与全栈工程实战

2026 年的现代后端架构师必须具备与大语言模型原生对话的能力。本阶段彻底剥离外部臃肿黑盒，从纯原生数学高维向量检索、大模型 Tool Calling 与 MCP (Model Context Protocol) 传输协议，到 SSE 生产级流式打字机交付，完成全栈大收官。

---

## 💡 核心工程心智与底层机制

1. **纯原生余弦相似度与微型向量 RAG 管道**：
   - 拒绝未入门先装笨重黑盒库，纯粹基于标准库 `math` 手写向量点积、模长与夹角余弦相似度计算；
   - 掌握知识库离线切片（Chunking）、高维向量索引匹配与检索增强 Prompt 动态注入全链路。
2. **大模型 Tool Calling 与 MCP (Model Context Protocol) 标准**：
   - 深刻理解大语言模型调用外部工具的本质（Schema 声明、模型决策意图、服务端执行工具并将结果回填对话历史）；
   - 掌握 Anthropic 主导的现代智能体开放标准 MCP 协议，构建标准化工具通信服务器。
3. **SSE（Server-Sent Events）大模型流式长连接推送**：
   - 彻底打破传统请求-响应模式对于长时间推理大模型的阻塞；
   - 掌握基于标准 HTTP/1.1 `text/event-stream` 的持续单向事件流推送，掌握心跳保活、客户端断线异常熔断与生产资源安全释放。

---

## 🗺️ 阶段专题导航

| 专题目录 | 核心原语 | 关键掌握目标 |
| :--- | :--- | :--- |
| **[01-vector-rag-pipeline-primitives](./01-vector-rag-pipeline-primitives/)** | 原生数学向量 RAG 管道 | 纯原生实现高维余弦相似度比对、Top-K 语义召回与 Prompt 增强注入 |
| **[02-agent-tool-calling-and-mcp](./02-agent-tool-calling-and-mcp/)** | 智能体 Tool Calling 与 MCP | 掌握大模型工具调用状态机、JSON Schema 契约与 MCP 协议编排 |
| **[03-sse-streaming-and-production-cap](./03-sse-streaming-and-production-cap/)** | SSE 流式推送与收官服务 | 掌握 HTTP text/event-stream 长连接、打字机逐字推流与高并发治理 |

---

## 🚀 统一运行验证

```bash
uv run python 09-ai-primitives-and-capstone/01-vector-rag-pipeline-primitives/main.py
uv run python 09-ai-primitives-and-capstone/02-agent-tool-calling-and-mcp/main.py
uv run python 09-ai-primitives-and-capstone/03-sse-streaming-and-production-cap/main.py
```
