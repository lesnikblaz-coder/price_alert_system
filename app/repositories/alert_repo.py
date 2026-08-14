from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from collections.abc import Sequence
from datetime import datetime, timezone

from app.models import Alert
from app.enums import AlertStatus


class AlertRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, alert: Alert) -> Alert:
        self.session.add(alert)
        await self.session.commit()
        await self.session.refresh(alert)
        return alert

    async def get_by_id(
            self,
            alert_id: UUID,
            user_id: UUID
    ) -> Alert | None:
        result = await self.session.execute(
            select(Alert).where(
                Alert.id == alert_id,
                Alert.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: UUID) -> Sequence[Alert]:
        result = await self.session.execute(
            select(Alert).where(Alert.user_id == user_id)
        )

        return result.scalars().all()

    async def get_active_by_symbol(self, symbol: str) -> Sequence[Alert]:
        result = await self.session.execute(
            select(Alert).where(
                Alert.symbol == symbol,
                Alert.status == AlertStatus.ACTIVE
            )
        )

        return result.scalars().all()

    async def get_active(self) -> Sequence[Alert]:
        result = await self.session.execute(
            select(Alert).where(
                Alert.status == AlertStatus.ACTIVE
            )
        )

        return result.scalars().all()

    async def update_status(self, alert: Alert, status: AlertStatus) -> Alert:
        alert.status = status

        if status == AlertStatus.TRIGGERED:
            alert.triggered_at = datetime.now(timezone.utc)

        await self.session.commit()
        await self.session.refresh(alert)

        return alert