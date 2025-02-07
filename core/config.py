from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # MySQL settings
    MYSQL_URL: str

    # Snowflake settings
    SNOWFLAKE_ACCOUNT: str
    SNOWFLAKE_USER: str
    SNOWFLAKE_PASSWORD: str
    SNOWFLAKE_DATABASE: str
    SNOWFLAKE_SCHEMA: str
    SNOWFLAKE_WAREHOUSE: str

    # JWT settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
