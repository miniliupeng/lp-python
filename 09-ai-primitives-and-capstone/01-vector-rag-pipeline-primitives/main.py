"""专题 01: 纯标准库 60 行极简向量 RAG 管道核心原语

剥离任何第三方臃肿库，纯粹基于标准库 math 实现余弦相似度计算、
Top-K 向量语义召回，并格式化组装企业级上下文增强 Prompt。
"""

import math


def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """计算两个高维稠密向量的夹角余弦相似度 (纯原生数学实现)."""
    dot_product = sum(a * b for a, b in zip(v1, v2, strict=True))
    norm_v1 = math.sqrt(sum(a * a for a in v1))
    norm_v2 = math.sqrt(sum(b * b for b in v2))
    if norm_v1 == 0.0 or norm_v2 == 0.0:
        return 0.0
    return dot_product / (norm_v1 * norm_v2)


class TinyVectorStore:
    """微型内存向量数据库: 负责高维空间语义距离比对与 Top-K 召回."""

    def __init__(self) -> None:
        self.documents: list[dict[str, object]] = []

    def add_document(self, doc_id: str, content: str, embedding: list[float]) -> None:
        self.documents.append({"id": doc_id, "content": content, "vec": embedding})

    def search_top_k(
        self, query_vec: list[float], k: int = 1
    ) -> list[dict[str, object]]:
        """基于余弦相似度暴力全量匹配最相似的 Top-K 知识切片."""
        scored = []
        for doc in self.documents:
            vec = doc["vec"]  # type: ignore[assignment]
            score = cosine_similarity(query_vec, vec)  # type: ignore[arg-type]
            scored.append({"doc": doc, "score": score})

        # 按相似度降序排序提取前 K 项
        scored.sort(key=lambda x: x["score"], reverse=True)  # type: ignore[arg-type]
        return [item["doc"] for item in scored[:k]]  # type: ignore[misc]


def main() -> None:
    print("=== [08-01] 纯原生极简向量 RAG 管道原语实操 ===")
    store = TinyVectorStore()

    # 1. 知识库预热: 注册内部文档及其模拟 Embedding 向量 (演示 3 维简化语义空间)
    store.add_document("doc-01", "FastAPI 基于 ASGI 架构提供高并发", [0.95, 0.10, 0.20])
    store.add_document(
        "doc-02", "Python 垃圾回收采用引用计数与分代收集", [0.10, 0.92, 0.15]
    )
    store.add_document(
        "doc-03", "Kubernetes 滚动更新依赖 SIGTERM 优雅停机", [0.20, 0.15, 0.90]
    )

    # 2. 模拟用户提问: "如何评估 Python 内存管理机制？" (语义向量偏向 doc-02)
    query_text = "如何评估 Python 内存管理机制？"
    user_query_vec = [0.12, 0.88, 0.18]

    # 3. 检索最相关的知识切片并组装增强 Prompt
    top_docs = store.search_top_k(user_query_vec, k=1)
    retrieved_content = top_docs[0]["content"]

    enhanced_prompt = (
        "【已知背景】: " + str(retrieved_content) + "\n【问题】: " + query_text
    )

    print("  • 成功召回最相关文档片段:")
    print(f"    -> [{top_docs[0]['id']}]: {retrieved_content}")
    print("  • 最终组装产出的 RAG 增强 Prompt:")
    print("  • 增强 Prompt:", enhanced_prompt)

    assert top_docs[0]["id"] == "doc-02", "向量空间余弦夹角计算必须精准命中 doc-02"
    print("✅ 纯原生微型向量 RAG 检索链路验证通过。")


if __name__ == "__main__":
    main()
