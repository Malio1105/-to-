import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application Settings (Load from .env)"""

    # ==================== #
    #      Core Config      #
    # ==================== #
    APP_NAME: str = "AD_caregiver"
    DEBUG: bool = False
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # 我们应该没有必要生成应用的API API_V1_STR = "/api/v1"

    # ==================== #
    #   Voice Service Config  #
    # ==================== #
    TTS_API_KEY: str = "sk-swldhdfbzrwtesarrhxwbovcivpzezfshaxvcxrtwvdzylss"  # 更新API密钥
    TTS_BASE_URL: str = "https://api.siliconflow.cn/v1"

    # ==================== #
    #  Chat Engine Config   #
    # ==================== #
    DEEPSEEK_API_KEY: str = "sk-7d54d72c0a314c45ae838b4ea422d152"   
    DEEPSEEK_API_URL: str = "https://api.deepseek.com/v1/chat/completions"

    # ==================== #
    #    Database Config    #
    # ==================== #
    DATABASE_URI: str = "mysql+pymysql://root:050729@localhost/app_db"
    DB_HOST: str = "localhost"
    DB_USER: str = "root"
    DB_PASSWORD: str = "050729"
    DB_NAME: str = "app_db"
    DB_PORT: int = 3306
    DB_CHARSET: str = "utf8mb4"

    # ==================== #
    #      CORS Config      #
    # ==================== #
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }


# Global settings instance
settings = Settings() 
