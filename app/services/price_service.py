import httpx

from decimal import Decimal

from app.clients.price_client import PriceClient
from app.schemas import PriceResponse
from app.logging_config import logger


class PriceService:
    def __init__(self, client: PriceClient):
        self.client = client

    async def get_symbol_price(self, symbol: str) -> PriceResponse | None:
        dict_response = await self.client.get_quote(symbol)

        if not dict_response:
            return None

        return PriceResponse.model_validate(dict_response)


    async def get_prices(self, symbols: set[str]) -> dict[str, Decimal]:
        prices = {}

        for symbol in symbols:
            try:
                dict_response = await self.client.get_quote(symbol)

                if dict_response:
                    prices[symbol] = PriceResponse.model_validate(dict_response).price

            except Exception as e:
                logger.error("Failed to fetch %s: %s", symbol, e)

        return prices

    @classmethod
    async def create(cls, api_key: str) -> "PriceService":
        # factory method for when there's no app.state to inject from
        http_client = httpx.AsyncClient(
            base_url="https://finnhub.io/api/v1",
            headers={"X-Finnhub-Token": api_key},
            timeout=5.0
        )

        return cls(client=PriceClient(http_client))

    async def __aenter__(self):
        ...

    async def __aexit__(self, *args):
        ...