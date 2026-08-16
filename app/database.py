from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

from app.config import settings


class Base(AsyncAttrs, DeclarativeBase):
    pass


engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
    poolclass=NullPool # connections aren't retained by a pool and subsequently reused by another event loop
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)