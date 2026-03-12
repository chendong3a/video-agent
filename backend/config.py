"""
配置文件
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用配置"""
    
    # 基础配置
    APP_NAME: str = "视频智能体"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Redis配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    
    # Celery配置
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # 文件存储路径
    UPLOAD_DIR: str = "./storage/uploads"
    OUTPUT_DIR: str = "./storage/outputs"
    TEMP_DIR: str = "./storage/temp"
    MODEL_DIR: str = "./models"
    
    # API Keys
    MINIMAX_API_KEY: str = ""
    MINIMAX_GROUP_ID: str = ""
    
    # BiliNote配置
    BILINOTE_API_URL: str = "http://localhost:8001"
    
    # 模型配置
    WHISPER_MODEL: str = "large-v3"
    COSYVOICE_MODEL_PATH: str = "./models/cosyvoice3"
    MUSETALK_MODEL_PATH: str = "./models/musetalk"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
