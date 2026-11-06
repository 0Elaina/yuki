"""分组读取部署配置；数据库迁移可以独立使用 PostgreSQL 配置。"""

from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field, NonNegativeInt, PositiveFloat, PositiveInt, SecretStr, StringConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

BACKEND_DIR = Path(__file__).resolve().parents[3]
SOURCE_DIR = BACKEND_DIR / "src"
ENV_FILE = BACKEND_DIR / ".env"

type NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
type Port = Annotated[int, Field(ge=1, le=65535)]
type Password = Annotated[SecretStr, Field(min_length=1)]


class DeploymentSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        hide_input_in_errors=True,
    )


class AppSettings(DeploymentSettings):
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    http_host: NonEmptyString = "127.0.0.1"
    http_port: Port = 8000
    http_reload: bool = False
    cors_allow_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]


class PostgresSettings(DeploymentSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    host: NonEmptyString = "127.0.0.1"
    port: Port = 5432
    user: NonEmptyString = "postgres"
    password: Password
    db: NonEmptyString = "yuki"
    sslmode: Literal["disable", "allow", "prefer", "require", "verify-ca", "verify-full"] = (
        "disable"
    )
    pool_size: PositiveInt = 5
    max_overflow: NonNegativeInt = 5
    pool_timeout_seconds: PositiveFloat = 30
    connect_timeout_seconds: PositiveInt = 5

    @property
    def url(self) -> URL:
        # URL.create 负责转义密码等字段中的 URL 特殊字符。
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.db,
        )

    @property
    def connect_args(self) -> dict[str, str | int]:
        return {
            "connect_timeout": self.connect_timeout_seconds,
            "sslmode": self.sslmode,
            "options": "-c timezone=UTC",
        }


class RedisSettings(DeploymentSettings):
    model_config = SettingsConfigDict(env_prefix="REDIS_")

    host: NonEmptyString = "127.0.0.1"
    port: Port = 6379
    password: Password
    db: NonNegativeInt = 0
    connect_timeout_seconds: PositiveFloat = 5
    command_timeout_seconds: PositiveFloat = 3
