from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str = "secret"
    debug: bool = False
    db_url: str = "postgresql://postgres:password@localhost:5432/vara"

settings = Settings()