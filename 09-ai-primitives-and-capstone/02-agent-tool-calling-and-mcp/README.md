# 专题 02：AI Agent 函数调用（Tool Calling）与 MCP 协议规范核心

随着大模型从“文本对话机器人”演进为“自主智能体（Autonomous Agents）”，**函数调用（Tool Calling / Function Calling）** 赋予了大模型调用外部计算、操作数据库与检索实时互联网的能力。而由 Anthropic 提出并迅速成为全球标准的 **MCP（Model Context Protocol，模型上下文协议）**，则确立了 AI 应用与外部工具/数据源交互的通用总线。

---

## 一、 痛点驱动：专有 API 割裂与传统硬编码 Agent 的脆弱

1. **各厂商 Function Calling SDK 割裂**：
   - OpenAI, Anthropic, Google 各有一套专有的 Tool 定义与响应格式，导致上层 Agent 代码极度碎片化；
2. **工具扩展的强耦合维护成本**：
   - 传统的做法是将工具代码直接写死在 Web 服务内部，每新增一个外部数据源工具，就必须全量发布一次后端服务。

---

## 二、 机制解密：Tool Calling 决策闭环与 MCP 协议标准

```text
[ 大模型 Tool Calling 真实执行闭环 (模型自身绝不执行代码！) ]
  用户提问: "帮我查询用户 101 的账户余额"
         │
         ▼
  LLM 决策推理 ──> 产出结构化工具调用指令 (ToolCall JSON: name="query_balance", args={"uid": 101})
         │
         ▼ (回传给宿主宿主 Python 运行时)
  Python 宿主安全沙箱执行真实函数 ──> 拿到真实业务数据: {"balance": 999.0}
         │
         ▼ (作为 ToolResult 再次送入大模型)
  LLM 依据真实数据产出最终自然语言答复: "用户 101 的当前账户余额为 999.0 元"

[ MCP (Model Context Protocol) 统一总线 ]
  MCP Client (AI 应用 / Cursor / Claude)
         │  (通过 JSON-RPC 2.0 协议标准传输: stdio / SSE)
         ▼
  MCP Server (标准化暴露 Resources, Prompts, Tools)
```

1. **认知纠偏：大模型绝不会“自己执行代码”**：
   - 大模型本质只是一个基于上下文概率预测的文本补全引擎；
   - 所谓的 Tool Calling，是模型在遇到需要调用工具时，**按照预先告知的 JSON Schema 格式输出了一段包含函数名与参数的 JSON 文本**；真正的物理执行必须由外部 Python 宿主程序代为完成并回传结果。

---

## 三、 生产规范与安全红线

- **入参严格校验（Schema Validation）**：从大模型拿到的 JSON 参数必须无条件使用 Pydantic 再次执行类型与安全校验；
- **防范 Prompt 越权注入（Indirect Prompt Injection）**：给模型配置只读权限，危险写操作（如转账、删除数据）必须引入人机协同确认（Human-in-the-loop）。
