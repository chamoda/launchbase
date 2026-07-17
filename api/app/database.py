from typing import Annotated

from fastapi import Depends
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapper

from app.config import settings

async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=settings.SQLALCHEMY_ECHO,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, expire_on_commit=False
)


class Base(AsyncAttrs, DeclarativeBase):
    """subclasses will be converted to dataclasses"""


@event.listens_for(Mapper, "mapper_configured")
def _default_lazy_raise_on_sql(mapper, _):  # pyright: ignore[reportUnusedFunction]
    # Surface accidental lazy loads as a clear error instead of MissingGreenlet
    # in async contexts. Use selectin/joined eager loading or `awaitable_attrs`.
    for rel in mapper.relationships:
        if rel.lazy == "select":
            rel.lazy = "raise_on_sql"


async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


DBSession = Annotated[AsyncSession, Depends(get_db)]
