"""API routes ของ Nova Studio"""
from fastapi import APIRouter, Depends

from cloudforge_auth_core import Principal
from src.auth.dependencies import get_current_user, require_nova_query
from src.models.schemas import QueryRequest, QueryResponse
from src.rag.service import RAGService

router = APIRouter()


def get_rag_service() -> RAGService:
    """
    Dependency provider — override ใน main.py ตอน wiring จริง (ใส่ KnowledgeStudioClient
    และ AnthropicProvider ที่ config มาแล้ว) และ override ใน test ด้วย mock
    """
    raise NotImplementedError("ต้อง override ด้วย dependency_overrides ใน main.py")


@router.post("/query", response_model=QueryResponse)
async def query(
    request: QueryRequest,
    current_user: Principal = Depends(get_current_user),
    _: None = Depends(require_nova_query),
    rag_service: RAGService = Depends(get_rag_service),
) -> QueryResponse:
    """
    ต้องมี scope `nova:query` (Identity Contract v1)

    - token ไม่ถูกต้อง → 401
    - token ถูกแต่ไม่มี nova:query → 403
    - JWKS เข้าไม่ถึง → 503
    """
    return await rag_service.answer(request.question, top_k=request.top_k)


@router.get("/health")
async def health() -> dict:
    return {"status": "ok"}
