"""Nova Studio — FastAPI entrypoint"""
import os

from fastapi import FastAPI

from src.api.routes import get_rag_service, router
from src.llm.anthropic_provider import AnthropicProvider
from src.rag.knowledge_client import KnowledgeStudioClient
from src.rag.service import RAGService

app = FastAPI(title="CloudForge Nova Studio", version="0.2.0")
app.include_router(router)


def _build_rag_service() -> RAGService:
    knowledge_client = KnowledgeStudioClient(
        base_url=os.environ.get("KNOWLEDGE_STUDIO_URL", "http://localhost:8001")
    )
    llm_provider = AnthropicProvider(api_key=os.environ["ANTHROPIC_API_KEY"])
    return RAGService(knowledge_client=knowledge_client, llm_provider=llm_provider)


app.dependency_overrides[get_rag_service] = _build_rag_service
