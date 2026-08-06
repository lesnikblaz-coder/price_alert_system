from app import auth
from app.exceptions import custom
from app.repositories.user_repo import UserRepository
from app.models import User
from app.schemas import TokenResponse
from app.logging_config import logger


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.repo = user_repo

    async def register(self, email: str, password: str) -> TokenResponse:
        if await self.repo.get_by_email(email):
            raise custom.DuplicateEmailError()

        user = User(
            email=email,
            hashed_pw=auth.get_pw_hash(password)
        )

        user = await self.repo.create(user)

        logger.info(
            "New user registered | id:%s, email:%s", user.id, user.email
        )

        return TokenResponse(
            access_token=auth.get_token(user.id)
        )

    async def login(self, email: str, password: str) -> TokenResponse:
        user = await self.repo.get_by_email(email)

        if not user or not auth.verify_pw(password, user.hashed_pw):
            logger.warning(
                "Invalid login attempt for email:%s", email
            )

            raise custom.InvalidCredentialsError()

        logger.info(
            "User login successful | id:%s, email:%s", user.id, user.email
        )

        return TokenResponse(
            access_token=auth.get_token(user.id)
        )