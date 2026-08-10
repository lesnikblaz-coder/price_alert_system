from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from collections.abc import Sequence

from app.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.session.execute(
            select(User)
            .where(User.id == user_id)
        )

        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )

        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_id_with_alerts(self, user_id: UUID) -> User | None:
        result = await self.session.execute(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.alerts))
        )

        return result.scalar_one_or_none()

    async def get_users(self) -> Sequence[User]:
        result = await self.session.execute(
            select(User)
        )

        return result.scalars().all()