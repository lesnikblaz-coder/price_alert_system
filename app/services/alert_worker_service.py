import json

from redis import Redis
from decimal import Decimal

from app import enums
from app.repositories.alert_repo import AlertRepository
from app.services.price_service import PriceService
from app.services.alert_evaluator import should_trigger
from app.models import Alert


class AlertWorkerService:
    def __init__(
            self,
            alert_repo: AlertRepository,
            price_service: PriceService,
            redis: Redis
    ):
        self.alert_repo = alert_repo
        self.price_service = price_service
        self.redis = redis

    async def check_prices(self):

        # get active alerts from DB
        alerts = await self.alert_repo.get_active()

        # get needed symbols
        symbols = {alert.symbol for alert in alerts}

        # current prices from FHUB
        prices = await self.price_service.get_prices(symbols)

        for alert in alerts:
            if alert.symbol not in prices:
                continue

            current_price = prices[alert.symbol]

            key = f"price:{alert.symbol}"

            previous_price = self.redis.get(key)

            if previous_price is not None:
                previous_price = Decimal(previous_price)

            triggered = should_trigger(
                alert=alert,
                current_price=current_price,
                previous_price=previous_price
            )

            if triggered:
                # Update database
                await self.alert_repo.update_status(
                    alert=alert,
                    status=enums.AlertStatus.TRIGGERED
                )

                # Redis publish
                message = self.alert_message(
                    alert=alert,
                    current_price=current_price
                )

                self.redis.publish(
                    f"alert:user:{alert.user_id}",
                    json.dumps(message)
                )

            # save current price to redis for 300 seconds
            self.redis.set(
                key,
                str(current_price),
                ex=enums.RedisTTL.value
            )

    @staticmethod
    def alert_message(alert: Alert, current_price: Decimal):
        return {
                    "alert_id":str(alert.id),
                    "user_id":str(alert.user_id),
                    "symbol":alert.symbol,
                    "condition":alert.condition.value,
                    "target_price":str(alert.target_price),
                    "current_price":str(current_price)
                }