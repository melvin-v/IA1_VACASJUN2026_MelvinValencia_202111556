from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://smartbot:smartbot@db:5432/smartbot"
    secret_key: str = "cambia-esta-clave-secreta-en-produccion"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 120
    cors_origins: str = "*"
    bot_api_key: str = "cambia-esta-clave-interna-del-bot"


settings = Settings()
