# Roadmap — CloudForge Nova Studio

## Phase 1 (ปัจจุบัน — v0.1.0)

- [x] Scaffold repo ตาม Foundation checklist
- [x] Auth pattern มาตรฐาน (JWT) เหมือน Ingest/Knowledge Studio
- [ ] `POST /query`: RAG endpoint พื้นฐาน (เรียก Knowledge Studio search → ส่ง context ให้ LLM → คืนคำตอบ + แหล่งอ้างอิง)
- [ ] `LLMProvider` interface + `AnthropicProvider` implementation
- [ ] Unit test ครอบคลุม RAG service (mock Knowledge Studio client + mock LLM provider)

## Phase 2

- [ ] รองรับ conversation history (multi-turn) แทนที่จะเป็น single-shot query
- [ ] Provider ที่สอง (เช่น OpenAI) เพื่อพิสูจน์ว่า interface ยืดหยุ่นจริง
- [ ] Caching ผลลัพธ์ search ที่ซ้ำกัน
- [ ] Rate limiting ระดับ endpoint

## Phase 3 (รอ Security Studio)

- [ ] Agent orchestration: multi-step task ที่เรียกใช้ tool/studio อื่นเป็นลำดับขั้น
  - **บล็อกไว้ก่อน**: ต้องรอ Security Studio วางระบบสิทธิ์/ควบคุมการเรียก tool ก่อน ไม่ทำ agent ที่เรียกอะไรก็ได้แบบไม่มีการควบคุมสิทธิ์
- [ ] Audit log ของทุกคำตอบที่ LLM สร้าง (โยง Compliance Studio ในอนาคต)

## Phase 4+

- ตาม roadmap หลักของแพลตฟอร์ม: Security Studio → Compliance Studio
