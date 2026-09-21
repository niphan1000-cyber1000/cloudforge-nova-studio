"""JWT encode/decode helpers — pattern เดียวกับ Ingest Studio และ Knowledge Studio"""
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from src.auth.config import auth_settings


class TokenError(Exception):
    """เกิดขึ้นเมื่อ token ไม่ถูกต้องหรือหมดอายุ"""


def create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=auth_settings.jwt_expire_minutes
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, auth_settings.jwt_secret_key, algorithm=auth_settings.jwt_algorithm
    )


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            token,
            auth_settings.jwt_secret_key,
            algorithms=[auth_settings.jwt_algorithm],
        )
    except JWTError as exc:
        raise TokenError("Invalid or expired token") from exc
