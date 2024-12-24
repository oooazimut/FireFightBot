# from pathlib import Path

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# BASE_DIR = Path(__file__).resolve().parent


class ModbusSettings(BaseModel):
    host: str
    port: int


class Settings(BaseSettings):
    bot_token: SecretStr
    db_name: str
    modbus: ModbusSettings
    password: SecretStr


    @property
    def sqlite_async_dsn(self):
        return f"sqlite+aiosqlite:///{self.db_name}"
    
    @property
    def sqlite_dsn(self):
        return f"sqlite:///{self.db_name}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
