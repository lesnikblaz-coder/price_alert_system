import jwt

from datetime import datetime, timezone, timedelta
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID

from app.exceptions import custom
from app.config import settings


pwd_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_pw_hash(plain_pw: str) -> str:
    return pwd_hash.hash(plain_pw)

def verify_pw(plain_pw: str, hashed_pw: str) -> bool:
    return pwd_hash.verify(plain_pw, hashed_pw)

def get_token(user_id: UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload=payload,
        key=settings.secret_key,
        algorithm=settings.algorithm
    )

def decode_token(token: str) -> UUID:
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.secret_key,
            algorithms=[settings.algorithm]
        )

        return UUID(payload["sub"])

    except(jwt.InvalidTokenError, KeyError, ValueError):
        raise custom.InvalidTokenError()