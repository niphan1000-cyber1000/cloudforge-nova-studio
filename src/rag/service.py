"""
RAG service — แกนหลักของ Nova Studio v1

Flow: รับคำถาม -> เรียก Knowledge Studio search -> ประกอบ context -> ส่งให้ LLM -> คืนคำตอบ + แหล่งอ้างอิง
"""
from src.llm.provider import LLMProvider
from src.models.schemas import QueryResponse, SourceDocument
from src.rag.knowledge_client import KnowledgeStudioClient

PROMPT_TEMPLATE = """\
ตอบคำถามด้านล่างโดยอ้างอิงจากเอกสารที่ให้มาเท่านั้น ถ้าเอกสารที่ให้มาไม่พอตอบคำถาม \
ให้บอกตรงๆ ว่าไม่มีข้อมูลเพียงพอ อย่าเดาข้อมูลที่ไม่มีในเอกสาร

เอกสารอ้างอิง:
{context}

คำถาม: {question}
"""


class RAGService:
    def __init__(
        self, knowledge_client: KnowledgeStudioClient, llm_provider: LLMProvider
    ) -> None:
        self._knowledge_client = knowledge_client
        self._llm_provider = llm_provider

    async def answer(
        self, question: str, *, top_k: int = 5, auth_token: str | None = None
    ) -> QueryResponse:
        results = await self._knowledge_client.search(
            question, top_k=top_k, auth_token=auth_token
        )

        if not results:
            return QueryResponse(
                answer="ไม่พบเอกสารที่เกี่ยวข้องเพียงพอที่จะตอบคำถามนี้",
                sources=[],
            )

        context = "\n\n".join(
            f"[{i + 1}] (source: {r.get('source', 'unknown')})\n{r.get('text', '')}"
            for i, r in enumerate(results)
        )
        prompt = PROMPT_TEMPLATE.format(context=context, question=question)

        answer_text = await self._llm_provider.generate(prompt)

        sources = [
            SourceDocument(
                text=r.get("text", ""),
                source=r.get("source", "unknown"),
                score=r.get("score", 0.0),
            )
            for r in results
        ]
        return QueryResponse(answer=answer_text, sources=sources)
