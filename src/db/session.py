from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import new_session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session
