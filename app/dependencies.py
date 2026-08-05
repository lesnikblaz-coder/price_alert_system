import jwt

from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import Annotated
from uuid import UUID

from app.auth import oauth2_scheme, SECRET_KEY, ALGORITHM
from app.database import AsyncSessionLocal
from app.exceptions import custom
from app.repositories.user_repo import UserRepository


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

async def get_user_repository(session: SessionDep):
    return UserRepository(session)

UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]

async def get_current_user(user_repo: UserRepoDep, token: str = Depends(oauth2_scheme)):
    try:

        decoded_payload = jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id: UUID = decoded_payload["sub"]

    except(InvalidTokenError, KeyError, ValueError):
        raise custom.InvalidTokenError()

    user = await user_repo.get_by_id(user_id)
    if not user:
        raise custom.InvalidCredentialsError()

    return user