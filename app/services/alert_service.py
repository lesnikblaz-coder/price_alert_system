from uuid import UUID
from decimal import Decimal

from app.enums import AlertCondition
from app.repositories.alert_repo import AlertRepository
from app.models import Alert
from app.exceptions import custom


class AlertService:
    def __init__(self, alert_repo: AlertRepository):
        self.repo = alert_repo

    async def get_by_user(self, user_id: UUID) -> list[Alert]:
        return list(await self.repo.get_by_user(user_id))

    async def get_by_id(self, alert_id: UUID, user_id: UUID) -> Alert:
        alert = await self.repo.get_by_id(alert_id, user_id)

        if not alert:
            raise custom.AlertNotFoundError()

        return alert

    async def create(
            self,
            user_id: UUID,
            symbol: str,
            condition: AlertCondition,
            target_price: Decimal
    ) -> Alert:
        alert = Alert(
            user_id=user_id,
            symbol=symbol.upper(),
            condition=condition,
            target_price=target_price
        )

        return await self.repo.create(alert)

    async def get_active_by_symbol(self, symbol: str) -> list[Alert]:
        return list(
            await self.repo.get_active_by_symbol(
                symbol
            )
        )