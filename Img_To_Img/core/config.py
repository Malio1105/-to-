import os
from pydantic import field_validator, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """用户认证核心配置（从环境变量或.env加载）"""

    # ==================== #
    #     App 基础配置      #
    # ==================== #
    APP_NAME: str = "UserAuthAPI"
    DEBUG: bool = False

    # ==================== #
    #     JWT 配置         #
    # ==================== #
    # 重要！生产环境必须通过环境变量设置，不要用默认值
    SECRET_KEY: SecretStr = SecretStr(os.getenv("SECRET_KEY", "default-insecure-secret"))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # Token有效期默认1天

    # ==================== #
    #     数据库配置         #
    # ==================== #
    # 示例：mysql+pymysql://user:password@host:port/dbname
    DATABASE_URI: str = ""

    # 密码哈希配置
    PWD_HASH_ALGORITHM: str = "bcrypt"  # 密码哈希算法

    # ==================== #
    #     安全配置          #
    # ==================== #
    # 允许的跨域请求（按需配置）
    BACKEND_CORS_ORIGINS: list[str] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def validate_cors_origins(cls, v: str | list[str]) -> list[str]:
        """将字符串格式的CORS来源转换为列表"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # 忽略未定义的配置项


# 全局配置实例
settings = Settings()