from pydantic import BaseModel, EmailStr, Field, ConfigDict
from decimal import Decimal
from uuid import UUID
from datetime import datetime

from app.enums import TokenType, AlertCondition, AlertStatus


# ---------- Auth/User ----------
class UserCredentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class LoginRequest(UserCredentials): ...

class RegisterRequest(UserCredentials): ...

class TokenResponse(BaseModel):
    access_token: str
    token_type: TokenType = Field(default=TokenType.BEARER)


# ---------- Alert ----------
class AlertRequest(BaseModel):
    symbol: str = Field(max_length=8)
    condition: AlertCondition
    target_price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)

class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    symbol: str
    condition: AlertCondition
    target_price: Decimal
    created_at: datetime
    triggered_at: datetime | None
    status: AlertStatus


# ---------- Stock Symbols ----------
class PriceResponse(BaseModel):
    price: Decimal = Field(validation_alias="c")

class SymbolRequest(BaseModel):
    symbol: str = Field(max_length=8)