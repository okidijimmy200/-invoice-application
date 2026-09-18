import httpx


class ApiRunner:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get(self, path: str) -> httpx.Response:
        return httpx.get(
            f"{self.base_url}{path}",
            timeout=10.0,
        )

    def post(self, path: str, payload: dict) -> httpx.Response:
        return httpx.post(
            f"{self.base_url}{path}",
            json=payload,
            timeout=10.0,
        )