import jwt
import os

from datetime import datetime, timezone, timedelta
from pwdlib import PasswordHash
from dotenv import load_dotenv
from pathlib import Path
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID

from app.exceptions import custom


load_dotenv(Path(__file__).resolve().parent.parent / ".env")
secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    raise RuntimeError("SECRET_KEY not found")

SECRET_KEY = secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_pw_hash(plain_pw: str) -> str:
    return pwd_hash.hash(plain_pw)

def verify_pw(plain_pw: str, hashed_pw: str) -> bool:
    return pwd_hash.verify(plain_pw, hashed_pw)

def get_token(user_id: UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload=payload,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )

def decode_token(token: str) -> UUID:
    try:
        payload = jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return UUID(payload["sub"])

    except(jwt.InvalidTokenError, KeyError, ValueError):
        raise custom.InvalidTokenError()