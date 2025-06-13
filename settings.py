from pydantic import BaseModel, Json
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    DEBUG: bool
    db_host: str
    db_user: str
    db_password: str
    db_name: str
    db_port: int


    class Config:
        env_file = ".env"  # Specify the path to your .env file
        env_file_encoding = "utf-8"
    