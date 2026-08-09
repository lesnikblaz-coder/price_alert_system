from app.clients.price_client import PriceClient
from app.schemas import PriceResponse


class PriceService:
    def __init__(self, client: PriceClient):
        self.client = client

    async def get_prices(self, symbol: str) -> PriceResponse | None:
        dict_response = await self.client.get_prices(symbol)

        if not dict_response:
            return None

        return PriceResponse.model_validate(dict_response)