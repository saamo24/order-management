from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "order_management"
    api_title: str = "Order Management API"
    api_version: str = "1.0.0"
    api_description: str = "A microservice for managing orders, customers, and products"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    secret_key: str = "super-secret-key"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
