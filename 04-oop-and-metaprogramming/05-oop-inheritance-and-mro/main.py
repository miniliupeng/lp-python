"""专题 05: 多继承菱形继承、C3 线性化算法与 super() 协同链

演示菱形继承下通过 super() 协作式调用链确保顶级基类仅被初始化一次，
并动态打印检查类对象的 __mro__ 线性化顺序。
"""


class BaseService:
    """顶级抽象基类."""

    def __init__(self, **kwargs: object) -> None:
        print("    -> [BaseService] 核心资源初始化 (全局仅应触发 1 次)")
        super().__init__(**kwargs)


class LoggingMixin(BaseService):
    """日志增强混入组件."""

    def __init__(self, **kwargs: object) -> None:
        print("    -> [LoggingMixin] 日志审计切面就绪")
        super().__init__(**kwargs)


class AuthMixin(BaseService):
    """鉴权增强混入组件."""

    def __init__(self, **kwargs: object) -> None:
        print("    -> [AuthMixin] 权限令牌校验切面就绪")
        super().__init__(**kwargs)


class GatewayService(LoggingMixin, AuthMixin):
    """网关汇聚服务: 构成经典菱形多继承结构."""

    def __init__(self, service_id: str, **kwargs: object) -> None:
        print(f"  [GatewayService] 开始启动网关服务: {service_id}")
        super().__init__(**kwargs)
        self.service_id = service_id


def main() -> None:
    print("=== [03-05] 多继承 MRO 与 super() 协同调用链实操 ===")

    # 1. 打印 C3 线性化解析顺序 (MRO)
    mro_names = [cls.__name__ for cls in GatewayService.__mro__]
    print("  • GatewayService 的 MRO 线性化顺序:")
    print(f"    {mro_names}")
    assert mro_names == [
        "GatewayService",
        "LoggingMixin",
        "AuthMixin",
        "BaseService",
        "object",
    ]

    # 2. 实例化服务，观察调用输出
    print("  • 触发服务实例化调用流:")
    service = GatewayService("gw-us-east-1")
    assert service.service_id == "gw-us-east-1"

    print("✅ C3 线性化保证基类仅初始化一次，super() 协同链验证通过。")


if __name__ == "__main__":
    main()
