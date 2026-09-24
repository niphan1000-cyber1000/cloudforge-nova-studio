"""
HTTP-level auth tests สำหรับ Nova Studio — ก่อนหน้านี้ Nova ไม่มีเทสชุดนี้เลย
ทดสอบผ่าน TestClient จริง ยิงเข้า /query จริง (mock เฉพาะ RAGService)
"""
import time

import jwt as pyjwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

from src.auth import dependencies as auth_deps
from src.auth.config import auth_settings
from src.main import app
from src.rag.service import RAGService

_PRIVATE_KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
_PUBLIC_KEY = _PRIVATE_KEY.public_key()
_PRIVATE_PEM = _PRIVATE_KEY.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)


class _FakeSigningKey:
    def __init__(self, key):
        self.key = key


class _FakeRAGService:
    async def answer(self, question: str, *, top_k: int = 5):
        from src.models.schemas import QueryResponse
        return QueryResponse(answer="fake answer", sources=[])


@pytest.fixture(autouse=True)
def _jwks_patch(monkeypatch):
    monkeypatch.setattr(
        auth_deps._jwks_cache,
        "get_signing_key",
        lambda token: _FakeSigningKey(_PUBLIC_KEY),
    )


@pytest.fixture
def client():
    from src.api.routes import get_rag_service
    app.dependency_overrides[get_rag_service] = lambda: _FakeRAGService()
    yield TestClient(app)
    app.dependency_overrides.clear()


def _make_token(scope="nova:query", **overrides):
    now = int(time.time())
    claims = {
        "sub": "test-user",
        "iss": auth_settings.jwt_issuer,
        "aud": auth_settings.jwt_audience,
        "iat": now,
        "exp": now + 3600,
        "scope": scope,
    }
    claims.update(overrides)
    return pyjwt.encode(claims, _PRIVATE_PEM, algorithm="RS256")


def test_query_without_token_is_401(client):
    resp = client.post("/query", json={"question": "hi"})
    assert resp.status_code == 401


def test_query_with_garbage_token_is_401(client):
    resp = client.post(
        "/query", json={"question": "hi"},
        headers={"Authorization": "Bearer not-a-real-jwt"},
    )
    assert resp.status_code == 401


def test_query_with_wrong_scope_is_403(client):
    token = _make_token(scope="ingest:read")  # no nova:query
    resp = client.post(
        "/query", json={"question": "hi"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 403


def test_query_with_correct_scope_succeeds(client):
    token = _make_token(scope="nova:query")
    resp = client.post(
        "/query", json={"question": "hi"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["answer"] == "fake answer"


def test_deprecated_scopes_list_shape_is_rejected(client):
    """Regression coverage for the exact drift this contract exists to close."""
    now = int(time.time())
    claims = {
        "sub": "x", "iss": auth_settings.jwt_issuer, "aud": auth_settings.jwt_audience,
        "iat": now, "exp": now + 3600, "scopes": ["nova:query"],
    }
    token = pyjwt.encode(claims, _PRIVATE_PEM, algorithm="RS256")
    resp = client.post(
        "/query", json={"question": "hi"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 401
