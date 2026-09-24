"""FastAPI dependencies — ใช้ shared implementation จาก cloudforge-auth-core

ห้าม implement JWT verify / scope parse เองอีก (Foundation gate rule)
"""
from typing import Annotated

from fastapi import Depends

from cloudforge_auth_core import Principal, get_current_user, require_scope

from src.auth.config import auth_settings

# ---------------------------------------------------------------------------
# Wiring note (auth-core v1.1.0)
# ---------------------------------------------------------------------------
# auth-core exposes:
#   - get_current_user  → FastAPI dependency ที่ verify JWT (RS256+JWKS)
#   - require_scope(scope: str) → dependency factory สำหรับตรวจ scope
#   - Principal         → object ที่มี .sub / .iss / .aud / .scopes
#
# ถ้า public API ของ auth-core รับ config ผ่าน env / settings object
# แทน keyword arguments ให้ปรับบรรทัด Depends(...) ด้านล่างให้ตรง
# (issuer / audience / jwks_url ถูกอ่านจาก AUTH_* แล้ว)
# ---------------------------------------------------------------------------

# บังคับ scope ที่ endpoint นี้ใช้
require_nova_query = require_scope("nova:query")


async def current_principal(
    principal: Annotated[Principal, Depends(get_current_user)],
) -> Principal:
    """
    Verify JWT ตาม Identity Contract v1 แล้วคืน Principal

    Semantics (auth-core ≥1.1.0):
    - ไม่มี token / malformed / signature ผิด / exp / iss / aud ไม่ตรง → 401
    - JWKS endpoint เข้าไม่ถึง → 503
    - token ถูกแต่ไม่มี scope claim → authenticated + scopes=empty (ไม่ใช่ 401)
    - token ถูกแต่ scope ไม่พอ (ตรวจที่ require_scope) → 403
    """
    # auth-core อ่าน AUTH_JWT_ISSUER / AUTH_JWT_AUDIENCE / AUTH_JWKS_URL จาก env
    # (หรือตั้งผ่าน AuthSettings ของตัวเอง) — ค่า default อยู่ใน src/auth/config.py
    _ = auth_settings  # keep import used; values already in process env
    return principal


# Public names ที่ routes ใช้
get_current_user = current_principal  # noqa: F811 — re-export under stable name
