"""专题 02: Pydantic V2 核心数据契约、跨字段联动校验实战

基于 Pydantic V2 构建用户注册请求契约，实现单字段格式检查、
@model_validator 跨字段密码一致性联动校验，并展示结构化错误抛出。
"""

from pydantic import BaseModel, Field, ValidationError, model_validator


class UserRegisterRequest(BaseModel):
    """用户注册强契约模型."""

    username: str = Field(min_length=3, max_length=20, description="用户账号")
    email: str = Field(pattern=r"^[w.-]+@[w.-]+.w+$", description="安全邮箱")
    password: str = Field(min_length=8, description="原始密码")
    confirm_password: str = Field(min_length=8, description="确认密码")

    @model_validator(mode="after")
    def verify_password_match(self) -> "UserRegisterRequest":
        """跨字段联动校验: 验证两次输入的密码是否完全一致."""
        if self.password != self.confirm_password:
            raise ValueError("两次输入的密码不一致，校验阻断！")
        return self


def main() -> None:
    print("=== [05-02] Pydantic V2 强契约与跨字段联动校验实战 ===")

    # 1. 验证正向合法数据契约流转
    valid_payload = {
        "username": "architect_leo",
        "email": "leo@infra.tech",
        "password": "SecurePassword123",
        "confirm_password": "SecurePassword123",
    }
    user = UserRegisterRequest.model_validate(valid_payload)
    print(f"  • 合法实体校验成功: 用户名={user.username}, 邮箱={user.email}")
    dumped = user.model_dump(exclude={"password", "confirm_password"})
    print(f"  • 序列化导出快照:   {dumped}")

    # 2. 验证逆向跨字段密码不一致拦截
    invalid_payload = {**valid_payload, "confirm_password": "WrongPassword"}
    try:
        UserRegisterRequest.model_validate(invalid_payload)
        print("❌ 错误: 密码不一致未被成功拦截！")
    except ValidationError as exc:
        print("  • Pydantic 成功拦截跨字段不一致:")
        print(f"    {exc.errors()[0]['msg']}")

    print("✅ Pydantic V2 Rust 校验引擎与联动规则验证通过。")


if __name__ == "__main__":
    main()
