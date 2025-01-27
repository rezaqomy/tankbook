from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    APP_ENV: str = "development"
    DEBUG: bool = False
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()

EMAIL_REGEX = r"(^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$)"
IRAN_PHONE_NUMBER_REGEX = "^(\+98|0)?9\d{9}$"


