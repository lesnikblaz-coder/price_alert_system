from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request
from typing import Annotated

from app import auth
from app.database import AsyncSessionLocal
from app.repositories.user_repo import UserRepository
from app.repositories.alert_repo import AlertRepository
from app.services.auth_services import AuthService
from app.services.alert_service import AlertService
from app.models import User
from app.exceptions import custom
from app.clients.price_client import PriceClient
from app.services.price_service import PriceService
from app.services.user_service import UserService
from app.enums import UserRole


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

async def get_user_service(user_repo: UserRepoDep) -> UserService:
    return UserService(user_repo)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
AlertServiceDep = Annotated[AlertService, Depends(get_alert_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]


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


def required_roles(*roles):
    def checker(current_user: CurrentUserDep)  -> User:
        if current_user.role not in roles:
            raise custom.InsufficientPermissions()
        return current_user
    return checker

AdminLockDep = Annotated[User, Depends(required_roles(UserRole.ADMIN))]
StaffLockDep = Annotated[User, Depends(required_roles(UserRole.ADMIN, UserRole.STAFF))]


# ---------- Clients ----------
async def get_price_client(request: Request) -> PriceClient:
    return PriceClient(request.app.state.http_client)

PriceClientDep = Annotated[PriceClient, Depends(get_price_client)]


async def get_price_service(client: PriceClientDep):
    return PriceService(client)

PriceServiceDep = Annotated[PriceService, Depends(get_price_service)]