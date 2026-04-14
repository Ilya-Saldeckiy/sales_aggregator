from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Marketplace Aggregator"
    debug: bool = False
    currency_api_url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
    cache_ttl: int = 3600
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()