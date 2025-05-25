from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, max_length=100, description="密码")

class LoginResponse(BaseModel):
    """登录响应模型"""
    success: bool
    message: str
    data: Optional[dict] = None