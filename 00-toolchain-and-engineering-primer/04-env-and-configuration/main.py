"""专题 04: 环境变量安全加载、强类型转换与配置 Fail-Fast 契约

演示如何遵循 12-Factor 原则，从环境变量与本地 .env 加载配置，
进行布尔/数值强类型安全校验，并在关键项缺失时实现 Fail-Fast 阻断。
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """应用程序不可变全局配置契约."""

    app_env: str
    port: int
    debug: bool
    api_secret: str

    @classmethod
    def load_from_env(cls) -> "AppConfig":
        """从环境变量中提取并进行严格类型转换与边界校验."""
        env = os.getenv("APP_ENV", "development").lower()

        try:
            port = int(os.getenv("PORT", "8000"))
            if not (1024 <= port <= 65535):
                raise ValueError(f"端口必须在 1024~65535 范围内，当前值: {port}")
        except ValueError as exc:
            raise ValueError(f"PORT 环境变量格式非法: {exc}") from exc

        # 防范 bool("false") 恒为 True 的经典 Python 大坑
        debug_raw = os.getenv("DEBUG", "false").lower()
        debug = debug_raw in ("true", "1", "yes", "on")

        # 核心凭证必填校验 (Fail-Fast)
        secret = os.getenv("API_SECRET")
        if not secret:
            raise ValueError("关键凭证缺失: 必须显式配置 API_SECRET 环境变量！")

        return cls(app_env=env, port=port, debug=debug, api_secret=secret)

    def masked_secret(self) -> str:
        """对敏感数据进行日志脱敏处理."""
        if len(self.api_secret) <= 4:
            return "***"
        return f"{self.api_secret[:2]}****{self.api_secret[-2:]}"


def main() -> None:
    print("=== [00-04] 现代 12-Factor 配置加载与类型安全校验 ===")

    # 模拟外部注入环境变量
    os.environ["APP_ENV"] = "production"
    os.environ["PORT"] = "8080"
    os.environ["DEBUG"] = "false"
    os.environ["API_SECRET"] = "sk-prod-998877665544"

    config = AppConfig.load_from_env()
    print(f"  • 环境标识: {config.app_env}")
    print(f"  • 监听端口: {config.port} (类型: {type(config.port).__name__})")
    print(f"  • 调试模式: {config.debug} (类型: {type(config.debug).__name__})")
    print(f"  • 密钥脱敏: {config.masked_secret()}")
    print("✅ 配置加载成功，关键参数均通过强类型安全校验。")


if __name__ == "__main__":
    main()
