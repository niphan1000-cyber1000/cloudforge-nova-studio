"""Auth configuration — ใช้ cloudforge-auth-core ตาม Identity Contract v1

Studio ไม่เก็บ secret key และไม่ออก token เองอีกต่อไป
Config ชี้ไปที่ Identity Service (issuer / audience / JWKS)
"""
from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):
    """
    ค่าที่ Studio ต้องตั้งเพื่อ verify JWT จาก CloudForge Identity Service

    ตรงกับ Identity Contract v1:
    - algorithm บังคับ RS256 (อยู่ใน auth-core)
    - public key ดึงจาก JWKS เท่านั้น (ห้าม hardcode)
    """

    # Issuer ที่ Identity Service ใส่ใน claim "iss"
    jwt_issuer: str = "https://identity.cloudforge.internal"

    # Audience ที่ Studio expect ใน claim "aud"
    jwt_audience: str = "cloudforge-platform"

    # JWKS endpoint ของ Identity Service (auth-core จะ cache + refresh ตาม kid)
    jwks_url: str = "https://identity.cloudforge.internal/.well-known/jwks.json"

    class Config:
        env_file = ".env"
        env_prefix = "AUTH_"


auth_settings = AuthSettings()
