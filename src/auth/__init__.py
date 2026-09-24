"""Auth layer ของ Nova Studio — thin wrapper รอบ cloudforge-auth-core

Studio นี้ไม่ออก token เอง (ไม่มี create_access_token)
และไม่ implement JWT verify / scope parse เอง
"""
from src.auth.dependencies import get_current_user, require_nova_query

__all__ = ["get_current_user", "require_nova_query"]
