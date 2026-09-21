"""Unit tests สำหรับ RAGService — mock ทั้ง Knowledge Studio client และ LLM provider"""
import pytest

from src.llm.provider import LLMProvider
from src.rag.knowledge_client import KnowledgeStudioClient
from src.rag.service import RAGService


class FakeLLMProvider(LLMProvider):
    def __init__(self, canned_response: str) -> None:
        self._canned_response = canned_response
        self.last_prompt: str | None = None

    async def generate(self, prompt: str, *, max_tokens: int = 1024) -> str:
        self.last_prompt = prompt
        return self._canned_response


class FakeKnowledgeClient(KnowledgeStudioClient):
    def __init__(self, canned_results: list[dict]) -> None:
        self._canned_results = canned_results

    async def search(self, query, *, top_k=5, auth_token=None):
        return self._canned_results


@pytest.mark.asyncio
async def test_answer_with_results():
    knowledge_client = FakeKnowledgeClient(
        [{"text": "Nova Studio ทำ RAG", "source": "README.md", "score": 0.92}]
    )
    llm = FakeLLMProvider("Nova Studio ทำหน้าที่ RAG ตามที่ README ระบุไว้")
    service = RAGService(knowledge_client=knowledge_client, llm_provider=llm)

    result = await service.answer("Nova Studio ทำอะไร")

    assert result.answer == "Nova Studio ทำหน้าที่ RAG ตามที่ README ระบุไว้"
    assert len(result.sources) == 1
    assert result.sources[0].source == "README.md"
    assert "README.md" in llm.last_prompt


@pytest.mark.asyncio
async def test_answer_with_no_results():
    knowledge_client = FakeKnowledgeClient([])
    llm = FakeLLMProvider("ไม่ควรถูกเรียก")
    service = RAGService(knowledge_client=knowledge_client, llm_provider=llm)

    result = await service.answer("คำถามที่ไม่มีเอกสารรองรับ")

    assert result.sources == []
    assert "ไม่พบเอกสาร" in result.answer
    assert llm.last_prompt is None
