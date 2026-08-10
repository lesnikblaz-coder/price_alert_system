from app.repositories.user_repo import UserRepository
from app.models import User


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.repo = user_repo

    async def get_users(self) -> list[User]:
        return list(await self.repo.get_users())