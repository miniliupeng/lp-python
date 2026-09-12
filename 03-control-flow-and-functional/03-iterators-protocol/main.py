"""专题 03: 迭代器协议 (__iter__ 与 __next__) 与流式分页容器

实现一个自洽且符合 Python 官方协议的高可用分页拉取迭代器，
演示如何通过 O(1) 恒定内存平滑消费海量分布式分页数据流。
"""

from collections.abc import Iterator


class MockPagedDataSource:
    """模拟外部高并发分页数据存储 (如分库分表或下游 REST API)."""

    def __init__(self, total_items: int = 10, page_size: int = 3) -> None:
        self.total_items = total_items
        self.page_size = page_size

    def fetch_page(self, page_index: int) -> list[str]:
        """根据页码拉取一页数据."""
        start = page_index * self.page_size
        if start >= self.total_items:
            return []
        end = min(start + self.page_size, self.total_items)
        return [f"record-{i}" for i in range(start, end)]


class StreamPageIterator(Iterator[str]):
    """工业级流式分页迭代器: 保持 O(1) 内存开销顺序消费外部海量数据."""

    def __init__(self, data_source: MockPagedDataSource) -> None:
        self.source = data_source
        self.current_page = 0
        self.buffer: list[str] = []
        self.buffer_idx = 0

    def __iter__(self) -> "StreamPageIterator":
        return self

    def __next__(self) -> str:
        # 当前本地缓存页已耗尽，按需网络拉取下一页
        if self.buffer_idx >= len(self.buffer):
            self.buffer = self.source.fetch_page(self.current_page)
            self.buffer_idx = 0
            self.current_page += 1

            # 若下一页拉取为空，代表全量数据已消费完毕，发出协议终止信号
            if not self.buffer:
                raise StopIteration

        item = self.buffer[self.buffer_idx]
        self.buffer_idx += 1
        return item


def main() -> None:
    print("=== [02-03] 迭代器协议与流式分页容器实战 ===")
    source = MockPagedDataSource(total_items=8, page_size=3)
    stream_iter = StreamPageIterator(source)

    # 1. 使用原生 for 循环遍历 (底层自动触发 __iter__ 与 __next__)
    collected: list[str] = []
    for record in stream_iter:
        collected.append(record)

    print(f"  • 流式拉取记录总数: {len(collected)}")
    print(f"  • 全量记录快照:     {collected}")
    assert len(collected) == 8, "必须准确消费全部分页数据"

    # 2. 验证迭代器一次性耗尽特性
    try:
        next(stream_iter)
        print("❌ 错误: 迭代器耗尽后不应再产出数据")
    except StopIteration:
        print("  • 验证成功: 已耗尽的迭代器继续调用 next() 严格抛出 StopIteration")

    print("✅ 迭代器协议双方法契约验证通过。")


if __name__ == "__main__":
    main()
