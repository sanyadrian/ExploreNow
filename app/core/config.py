from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    app_name: str = "ExploreNow"
    app_version: str = "1.0"
    debug: bool = False

    google_api_key: str
    ticketmaster_api_key: str
    eventbrite_api_key: str
    database_url: str
    redis_url: str = "redis://localhost:6379"


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
settings = Settings()

