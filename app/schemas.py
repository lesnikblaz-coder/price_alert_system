from pydantic import BaseModel, EmailStr, Field

from app.enums import TokenType


# AUTH
class UserCredentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class LoginRequest(UserCredentials): ...

class RegisterRequest(UserCredentials): ...

class TokenResponse(BaseModel):
    access_token: str
    token_type: TokenType = Field(default=TokenType.BEARER)