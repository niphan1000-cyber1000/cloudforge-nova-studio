"""
Pluggable LLM provider interface

เพิ่ม provider ใหม่ (เช่น OpenAI) โดย implement ABC นี้ — ไม่ต้องแก้ core RAG logic
ที่อื่นเลย (ดู src/rag/service.py)
"""
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Interface กลางสำหรับเรียก LLM ไม่ว่าจะเป็นเจ้าไหน"""

    @abstractmethod
    async def generate(self, prompt: str, *, max_tokens: int = 1024) -> str:
        """ส่ง prompt ไปยัง LLM แล้วคืนข้อความคำตอบ (plain text)"""
        raise NotImplementedError
