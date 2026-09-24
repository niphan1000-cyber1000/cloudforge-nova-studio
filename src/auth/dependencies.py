"""
Thin binding layer over cloudforge_auth_core. Nova is a resource server
only -- it verifies tokens issued by the central Identity Service, it
never issues its own (no create_access_token / equivalent exists here on
purpose; do not re-add one). See CloudForge Identity Contract v1 §3.
"""
from cloudforge_auth_core import Principal, build_auth_dependencies
from cloudforge_auth_core.jwks import JWKSCache

from src.auth.config import build_auth_config

_jwks_cache = JWKSCache(build_auth_config())
get_current_user, require_scope = build_auth_dependencies(
    build_auth_config(), jwks_cache=_jwks_cache
)

__all__ = ["get_current_user", "require_scope", "Principal", "_jwks_cache"]
