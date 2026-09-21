"""Auth configuration — pattern เดียวกับ Ingest Studio และ Knowledge Studio ห้ามเบี่ยงเบน"""
from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    class Config:
        env_file = ".env"
        env_prefix = "JWT_"


auth_settings = AuthSettings()
