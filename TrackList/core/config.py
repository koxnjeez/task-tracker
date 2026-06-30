from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  GOOGLE_CLIENT_ID: str
  GOOGLE_CLIENT_SECRET: str

  JWT_SECRET: str
  JWT_TOKEN_EXPIRE_HOURS: int = 8
  JWT_ALGORITHM: str = "HS256"
  model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()