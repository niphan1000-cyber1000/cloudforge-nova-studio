# CloudForge Nova Studio

Studio ตัวที่สามของ CloudForge Platform — รับคำถามจากผู้ใช้ ดึงเอกสารที่เกี่ยวข้องจาก
Knowledge Studio (semantic search) แล้วส่งให้ LLM สร้างคำตอบแบบอ้างอิงแหล่งที่มา (RAG:
Retrieval-Augmented Generation) ตาม roadmap: Ingest → Knowledge → **Nova** → Security → Compliance

## Scope ของเวอร์ชันนี้ (v0.1.0)

- Endpoint เดียว: `POST /query` — รับคำถาม, เรียก Knowledge Studio search, ส่ง context ให้ LLM, คืนคำตอบ + รายการแหล่งอ้างอิง
- LLM provider เป็น **pluggable interface** (`src/llm/provider.py`) — ตอนนี้มี implementation เดียวคือ Anthropic (`src/llm/anthropic_provider.py`) เพิ่มเจ้าอื่นได้โดยไม่ต้องแก้ core logic
- ยังไม่มี agent orchestration / multi-step tool calling — วางแผนไว้เป็นเฟสถัดไป (ดู ROADMAP.md) หลัง Security Studio วางระบบสิทธิ์ให้ก่อน

## Local Dev

```
docker compose up --build
```

- API: http://localhost:8002 (host) → 8000 (container)
- ต้องตั้งค่า environment variables ก่อนรัน (ดู `.env.example`):
  - `ANTHROPIC_API_KEY`
  - `KNOWLEDGE_STUDIO_URL` (ค่า default: `http://localhost:8001`)
  - `JWT_SECRET_KEY`

## Auth

ใช้ pattern มาตรฐานเดียวกับ Ingest Studio และ Knowledge Studio ทุกไฟล์
(`src/auth/config.py`, `src/auth/jwt.py`, `src/auth/dependencies.py`) — ห้ามเบี่ยงเบนจาก pattern นี้

## เอกสารที่เกี่ยวข้อง

- [MASTER_INDEX.md](MASTER_INDEX.md) — ดัชนีเอกสารทั้งหมดของ repo นี้
- [ROADMAP.md](ROADMAP.md) — แผนพัฒนา
- [CHANGELOG.md](CHANGELOG.md) — ประวัติการเปลี่ยนแปลง
- CloudForge Platform Foundation repo — governance/OAS rules กลางที่ repo นี้ต้องทำตาม
