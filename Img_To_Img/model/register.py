from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    """用户注册请求模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, max_length=50, description="密码")
    email: str = Field(..., description="邮箱")
    phone: str = Field(..., description="手机号")
    role: int = Field(0, description="角色(0=用户，1=管理员)")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "testuser",
                "password": "123456",
                "email": "test@example.com",
                "phone": "13800138000",
                "role": 0
            }
        }

class UserResponse(BaseModel):
    """用户响应模型"""
    success: bool
    message: str
    data: Optional[dict] = None