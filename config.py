"""
Centralized configuration management for RoadFlow API.
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    """Database configuration settings."""

    # PostgreSQL settings
    postgres_url: str = Field(default="", env="POSTGRES_URL")

    # MongoDB settings
    mongo_uri: str = Field(default="mongodb://localhost:27017", env="MONGO_URI")
    mongo_db_name: str = Field(default="roadflow", env="MONGO_DB_NAME")

    # Redis settings
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_db: int = Field(default=0, env="REDIS_DB")
    redis_uri: str | None = Field(default=None, env="REDIS_URI")


class SecurityConfig(BaseSettings):
    """Security configuration settings."""

    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")


class AppConfig(BaseSettings):
    """Main application configuration."""

    app_name: str = Field(default="RoadFlow API", env="APP_NAME")
    environment: str = Field(default="development", env="ENV")
    debug: bool = Field(default=False, env="DEBUG")
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=3000, env="API_PORT")
    timezone: str = Field(default="America/Mexico_City", env="TZ")

    # AI/Agent settings
    default_model: str = Field(default="gemini-2.0-flash", env="DEFAULT_MODEL")


class EmailConfig(BaseSettings):
    """Email configuration settings."""

    resend_api_key: str | None = Field(default=None, env="RESEND_API_KEY")
    from_email: str = Field(default="noreply@roadflow.ai", env="FROM_EMAIL")


class Config:
    """Main configuration class combining all settings."""

    def __init__(self):
        self.database = DatabaseConfig()
        self.security = SecurityConfig()
        self.app = AppConfig()
        self.email = EmailConfig()

    def validate(self) -> None:
        """Validate required configuration values."""
        errors = []

        if not self.security.secret_key:
            errors.append("SECRET_KEY is required")

        if not self.database.postgres_url:
            errors.append("POSTGRES_URL is required")

        if errors:
            raise ValueError(f"Configuration validation failed: {', '.join(errors)}")


# Global configuration instance
config = Config()


def get_config() -> Config:
    """Get the global configuration instance."""
    return config
