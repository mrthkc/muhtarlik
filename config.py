from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_user: str
    db_pass: str
    db_port: int = 5432
    db_name: str

    model_config = SettingsConfigDict(env_file=".env")
