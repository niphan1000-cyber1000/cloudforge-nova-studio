"""Pydantic models สำหรับ request/response ของ Nova Studio API"""
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, description="คำถามจากผู้ใช้")
    top_k: int = Field(5, ge=1, le=20, description="จำนวนเอกสารที่ดึงมาจาก Knowledge Studio")


class SourceDocument(BaseModel):
    text: str
    source: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceDocument]
