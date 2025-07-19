from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import SessionModel


class SessionRepository:
    @staticmethod
    async def _get_last_session(
        session_id: str, session: AsyncSession
    ) -> SessionModel | None:
        query = (
            select(SessionModel)
            .where(SessionModel.session_id == session_id)
            .order_by(SessionModel.timestamp.desc())
            .limit(1)
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def _add_session(session_id: str, session: AsyncSession) -> None:
        new_session = SessionModel(session_id=session_id)
        session.add(new_session)
        await session.flush()
        await session.commit()

    @classmethod
    async def update_session(cls, session_id: str, session: AsyncSession) -> None:
        last = await cls._get_last_session(session_id, session)
        if not last or datetime.now() - last.timestamp > timedelta(minutes=30):
            await cls._add_session(session_id, session)
