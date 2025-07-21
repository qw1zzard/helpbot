from datetime import datetime

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.core.settings import get_settings


class Model(DeclarativeBase):
    pass


class SessionModel(Model):
    __tablename__ = 'sessions'
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[str]
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now)


settings = get_settings()
POSTGRES_URL = (
    f'postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}'
    f'@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}'
)

engine = create_async_engine(POSTGRES_URL)
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
