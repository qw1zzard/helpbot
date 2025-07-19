from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.schemas import History, HistoryMessage
from src.core.model import get_rag_answer
from src.db.database import new_session
from src.db.repository import SessionRepository

router = APIRouter(
    prefix='/api/v1',
    tags=['Answers'],
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session


def extract_user_input(history: list[HistoryMessage]) -> str:
    for msg in reversed(history):
        if msg.role == 'user':
            return msg.content
    raise HTTPException(status_code=400, detail='User message not found')


@router.post('/get_answer/')
async def get_answer(
    query: History, session: AsyncSession = Depends(get_session)
) -> dict[str, str]:
    await SessionRepository.update_session(query.session_id, session)

    user_input = extract_user_input(query.history)

    return {'answer': get_rag_answer(query.session_id, user_input)}
