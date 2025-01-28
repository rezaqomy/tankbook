from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    APP_ENV: str = "development"
    DEBUG: bool = False
    DISPATCH_JWT_SECRET: str
    DISPATCH_JWT_ALG: str
    DISPATCH_JWT_EXP: int

    class Config:
        env_file = ".env"

settings = Settings()

EMAIL_REGEX = r"(^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$)"
IRAN_PHONE_NUMBER_REGEX = "^(\+98|0)?9\d{9}$"


