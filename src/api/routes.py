"""API routes ของ Nova Studio"""
from fastapi import APIRouter, Depends

from src.auth.dependencies import get_current_user
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
    current_user: dict = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service),
) -> QueryResponse:
    return await rag_service.answer(request.question, top_k=request.top_k)


@router.get("/health")
async def health() -> dict:
    return {"status": "ok"}
