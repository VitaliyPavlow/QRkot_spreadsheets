from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = "API для сервиса QR-кот."
    description: str = "Сервис для приема пожертвований."
    database_url: str = "sqlite+aiosqlite:///./test.db"
    secret: str = "SECRET"
    first_superuser_email: Optional[EmailStr] = "admin@admin.com"
    first_superuser_password: Optional[str] = "password"
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_prefix = "charity_"
        env_file = ".env"


settings = Settings()
