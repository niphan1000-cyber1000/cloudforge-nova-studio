"""Client สำหรับเรียก semantic search ของ Knowledge Studio (studio ตัวที่ 2)"""
import httpx


class KnowledgeStudioClient:
    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    async def search(
        self, query: str, *, top_k: int = 5, auth_token: str | None = None
    ) -> list[dict]:
        """
        เรียก endpoint search ของ Knowledge Studio

        คืนค่าเป็น list ของ dict รูปแบบ {"text": str, "source": str, "score": float}
        NOTE: path/response shape ตรงนี้อ้างอิงตาม API ที่ตกลงกันไว้ — ถ้า Knowledge Studio
        เปลี่ยน contract ต้องอัปเดตที่นี่ด้วย
        """
        headers = {}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                f"{self._base_url}/search",
                json={"query": query, "top_k": top_k},
                headers=headers,
            )
            response.raise_for_status()
            return response.json().get("results", [])
