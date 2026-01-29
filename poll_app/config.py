from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModbusSettings(BaseModel):
    host: str
    port: int


class PGSettings(BaseModel):
    host: str
    port: str
    db_name: str
    user: str
    passw: str


class Settings(BaseSettings):
    modbus: ModbusSettings
    pg: PGSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
