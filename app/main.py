import httpx
import redis.asyncio as aioredis

from uuid import UUID
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from contextlib import asynccontextmanager

from app import schemas
from app import dependencies
from app.config import settings
from app.exceptions.handlers import register_exception_handlers
from app.models import Alert, User
from app.enums import AlertStatus


@asynccontextmanager
async def lifespan(app: FastAPI):
    http_client = httpx.AsyncClient(
        base_url="https://finnhub.io/api/v1",
        headers={
            "X-Finnhub-Token": settings.fhub_api_key,
        },
        timeout=5,
    )

    async_redis = aioredis.from_url(
        settings.redis_url,
        decode_responses=True,
    )

    app.state.http_client = http_client
    app.state.async_redis = async_redis

    try:
        yield
    finally:
        await http_client.aclose()
        await async_redis.aclose()


app = FastAPI(lifespan=lifespan)


register_exception_handlers(app)


# ---------- Root ----------
@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"status": "ok"}


# ---------- Auth ----------
@app.post("/auth/login", response_model=schemas.TokenResponse)
async def login(
        service: dependencies.AuthServiceDep,
        request: schemas.LoginRequest
) -> schemas.TokenResponse:
    return await service.login(
        request.email,
        request.password
    )

@app.post("/auth/register", response_model=schemas.TokenResponse)
async def register(
        service: dependencies.AuthServiceDep,
        request: schemas.RegisterRequest
) -> schemas.TokenResponse:
    return await service.register(
        request.email,
        request.password
    )

@app.post("/auth/token", response_model=schemas.TokenResponse)
async def token(
        service: dependencies.AuthServiceDep,
        form_data: OAuth2PasswordRequestForm = Depends()
) -> schemas.TokenResponse:
    return await service.login(
        form_data.username,
        form_data.password
    )


# ---------- Users (admin*) ----------
@app.get("/users", response_model=list[schemas.UserResponse])
async def get_users(
        service: dependencies.UserServiceDep,
        _: dependencies.AdminLockDep
) -> list[User]:
    return await service.get_users()


# ---------- Alerts ----------
@app.get("/alerts", response_model=list[schemas.AlertResponse])
async def get_alerts(
        service: dependencies.AlertServiceDep,
        user: dependencies.CurrentUserDep
) -> list[Alert]:
    return await service.get_by_user(user.id)

@app.post("/alerts", response_model=schemas.AlertResponse)
async def create_alert(
        service: dependencies.AlertServiceDep,
        user: dependencies.CurrentUserDep,
        request: schemas.AlertRequest
) -> Alert:
    return await service.create(
        user_id=user.id,
        symbol=request.symbol,
        condition=request.condition,
        target_price=request.target_price
    )

@app.get("/alerts/{alert_id}", response_model=schemas.AlertResponse)
async def get_alert_by_id(
        alert_id: UUID,
        service: dependencies.AlertServiceDep,
        user: dependencies.CurrentUserDep
) -> Alert:
    return await service.get_by_id(
        alert_id=alert_id,
        user_id=user.id
    )

@app.put("/alerts/{alert_id}", response_model=schemas.AlertResponse)
async def deactivate_alert(
        alert_id: UUID,
        service: dependencies.AlertServiceDep,
        user: dependencies.CurrentUserDep
) -> Alert:
    return await service.update_status(
        alert_id=alert_id,
        user_id=user.id,
        status=AlertStatus.CANCELLED
    )


# ---------- Stock Price ----------
@app.post("/price", response_model=schemas.PriceResponse)
async def get_price(request: schemas.SymbolRequest, service: dependencies.PriceServiceDep):
    return await service.get_symbol_price(request.symbol)