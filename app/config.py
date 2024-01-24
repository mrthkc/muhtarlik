from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str
    db_user: str
    db_pass: str
    db_port: int = 5432
    db_name: str
    smtp_host: str
    smtp_port: int
    smtp_pass: str
    sender_mail: str

    model_config = SettingsConfigDict(env_file=".env")
