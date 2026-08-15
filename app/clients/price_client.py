import httpx


class PriceClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get_quote(self, symbol: str):
        params = {
            "symbol": symbol
        }

        response = await self.client.get(
            url="/quote",
            params=params
        )

        response.raise_for_status()

        return response.json()

    async def close(self):
        await self.client.aclose()