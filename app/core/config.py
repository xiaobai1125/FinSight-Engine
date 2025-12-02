from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "FinSight Engine"
    API_V1_STR: str = "/api/v1"

    # 允许跨域
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # ================= 配置你的 DeepSeek =================
    # 填入 Key (不要带空格)
    OPENAI_API_KEY: str = "********************"
    # DeepSeek 官方地址
    OPENAI_BASE_URL: str = "https://api.deepseek.com"
    # 模型名称
    MODEL_NAME: str = "deepseek-chat"
    # ===================================================

    # 忽略环境变量文件，强制使用上述配置
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()