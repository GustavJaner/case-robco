# app/config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Loads .env at startup.

class Settings(BaseSettings):
  """Configuration settings for the application."""
  DEBUG_MODE: bool = False
  # DATABASE_URL: str = "postgresql+asyncpg://robotuser:password@localhost:5432/robotdb"
  # FRONTEND_ORIGIN: str = "http://localhost:3000"

  class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"

settings = Settings()
