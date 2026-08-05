from app.repositories.user_repo import UserRepository


async def register(user_repo: UserRepository, email: str, password: str) -> None:
    if await user_repo.