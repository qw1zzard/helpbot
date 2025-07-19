from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.schemas import History
from src.core.model import get_rag_answer
from src.db.repository import SessionRepository
from src.db.session import get_session

router = APIRouter(
    prefix='/api/v1',
    tags=['Answers'],
)


@router.post('/get_answer/')
async def get_answer(
    query: History, session: AsyncSession = Depends(get_session)
) -> dict[str, str]:
    await SessionRepository.update_session(query.session_id, session)

    user_input = next(
        (msg.content for msg in query.history if msg.role == 'user'), None
    )

    if not user_input:
        raise HTTPException(status_code=400, detail='User message not found')

    return {'answer': get_rag_answer(query.session_id, user_input)}
