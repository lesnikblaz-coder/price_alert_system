from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import Annotated

from app import auth
from app.database import AsyncSessionLocal
from app.repositories.user_repo import UserRepository
from app.services.auth_services import AuthService
from app.models import User
from app.exceptions import custom


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)

UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]



async def get_auth_service(user_repo: UserRepoDep) -> AuthService:
    return AuthService(user_repo)


TokenDep = Annotated[str, Depends(auth.oauth2_scheme)]

async def get_current_user(
        user_repo: UserRepoDep,
        token: TokenDep
) -> User:
    user_id = auth.decode_token(token)
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise custom.InvalidCredentialsError()
    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]