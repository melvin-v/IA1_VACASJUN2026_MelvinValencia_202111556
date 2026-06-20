from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "SmartInvoice"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql+psycopg2://smartinvoice:smartinvoice@db:5432/smartinvoice"

    # JWT
    JWT_SECRET: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Archivos / OCR
    UPLOAD_DIR: str = "uploads"
    ALLOWED_EXTENSIONS: set[str] = {"pdf", "jpg", "jpeg", "png"}
    TESSERACT_CMD: str | None = None
    TESSERACT_LANG: str = "spa+eng"
    PDF_DPI: int = 300

    # RPA (Playwright). El RPA visita el formulario del "sistema simulado".
    BASE_URL: str = "http://localhost:8000"
    RPA_HEADLESS: bool = True

    # Correo (SMTP). Si SMTP_HOST esta vacio, el envio se omite con aviso.
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_FROM: str = "smartinvoice@example.com"
    SMTP_TLS: bool = True

    AUTO_CREATE_TABLES: bool = True


settings = Settings()
