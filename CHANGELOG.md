# Changelog

รูปแบบอ้างอิง [Keep a Changelog](https://keepachangelog.com/) และ [Semantic Versioning](https://semver.org/)

## [0.2.0] - 2026-09-24

### Changed
- **Auth migration → Identity Contract v1 + cloudforge-auth-core v1.1.0**
  - ลบ `create_access_token()` และ HS256 local secret ออกทั้งหมด
  - เปลี่ยนมาใช้ RS256 + JWKS จาก Identity Service (ผ่าน `cloudforge-auth-core`)
  - บังคับ scope `nova:query` บน `POST /query` (403 เมื่อ scope ไม่พอ)
  - รองรับ 503 เมื่อ JWKS endpoint เข้าไม่ถึง
  - OpenAPI ประกาศ 401 + 403 (+ 503 แนะนำ) ครบตาม Foundation gate rule
- `.env.example` เปลี่ยนจาก `JWT_SECRET_KEY` → `AUTH_JWT_ISSUER` / `AUTH_JWT_AUDIENCE` / `AUTH_JWKS_URL`

### Removed
- `src/auth/jwt.py` (local encode/decode)
- Dependency `python-jose` (ย้ายไปอยู่ใน auth-core)

## [0.1.0] - Unreleased

### Added
- Scaffold repo ตาม Foundation Repository Standards Checklist ครบ
- Auth pattern มาตรฐาน (`src/auth/`) เหมือน Ingest Studio และ Knowledge Studio
- โครง RAG service: `LLMProvider` interface, `AnthropicProvider`, Knowledge Studio client, `POST /query` endpoint
- Docker Compose สำหรับรันในเครื่อง
