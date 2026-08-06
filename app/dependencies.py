from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import Annotated

from app.database import AsyncSessionLocal
from app.repositories.user_repo import UserRepository
from app.services.auth_services import AuthService
from app.models import User
from app.auth import oauth2_scheme


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)

UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]



async def get_auth_service(user_repo: UserRepoDep) -> AuthService:
    return AuthService(user_repo)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


TokenDep = Annotated[str, Depends(oauth2_scheme)]

async def get_current_user(
        service: AuthServiceDep,
        token: TokenDep
) -> User:
    return await service.get_current_user(token)