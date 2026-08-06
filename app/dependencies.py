from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import Annotated

from app import auth
from app.database import AsyncSessionLocal
from app.repositories.user_repo import UserRepository
from app.repositories.alert_repo import AlertRepository
from app.services.auth_services import AuthService
from app.services.alert_service import AlertService
from app.models import User
from app.exceptions import custom



# ---------- Session ----------
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]



# ---------- Repositories ----------
async def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)

async def get_alert_repository(session: SessionDep) -> AlertRepository:
    return AlertRepository(session)

UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]
AlertRepoDep = Annotated[AlertRepository, Depends(get_alert_repository)]


# ---------- Services ----------
async def get_auth_service(user_repo: UserRepoDep) -> AuthService:
    return AuthService(user_repo)

async def get_alert_service(alert_repo: AlertRepoDep) -> AlertService:
    return AlertService(alert_repo)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
AlertServiceDep = Annotated[AlertService, Depends(get_alert_service)]



# ---------- Auth ----------
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