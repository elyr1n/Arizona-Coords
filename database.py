from typing import Annotated

from fastapi import Depends

from sqlalchemy import JSON
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine("sqlite+aiosqlite:///klad.db")
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with async_session_maker() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class KladModel(Base):
    __tablename__ = "klad"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str]
    x: Mapped[int]
    y: Mapped[int]
    z: Mapped[int]
    loot: Mapped[list] = mapped_column(JSON)
    time: Mapped[str]


async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
