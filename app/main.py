from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas
from app.dependencies import AuthServiceDep
from app.exceptions.handlers import register_exception_handlers


# app lifespan


app = FastAPI()
register_exception_handlers(app)


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/auth/login", response_model=schemas.TokenResponse)
async def login(
        service: AuthServiceDep,
        request: schemas.LoginRequest
) -> schemas.TokenResponse:
    return await service.login(
        request.email,
        request.password
    )

@app.post("/auth/register", response_model=schemas.TokenResponse)
async def register(
        service: AuthServiceDep,
        request: schemas.RegisterRequest
) -> schemas.TokenResponse:
    return await service.register(
        request.email,
        request.password
    )

@app.post("/auth/token", response_model=schemas.TokenResponse)
async def token(
        service: AuthServiceDep,
        form_data: OAuth2PasswordRequestForm = Depends()
) -> schemas.TokenResponse:
    return await service.login(
        form_data.username,
        form_data.password
    )