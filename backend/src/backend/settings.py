from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='./src/backend/.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str
    JWT_ISSUER: str
    JWT_AUDIENCE: str
    JWT_ALGORITHM: str
    JWT_SECRET: str
    JWT_TTL_MINUTES: int
