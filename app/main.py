from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas
from app.dependencies import SessionDep



# app lifespan


app = FastAPI()


@app.post("/auth/login", response_model=schemas.TokenResponse)
async def login(session: SessionDep, request: schemas.LoginRequest) -> schemas.TokenResponse:
    ...

@app.post("/auth/register", response_model=schemas.TokenResponse)
async def register(session: SessionDep, request: schemas.RegisterRequest) -> schemas.TokenResponse:
    ...

@app.post("/auth/token", response_model=schemas.TokenResponse)
async def token(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()) -> schemas.TokenResponse:
    ...