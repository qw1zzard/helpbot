from api.schemas import History
from core.model import get_rag_answer
from db.repository import SessionRepository
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix='/api/v1',
    tags=['Answers'],
)


@router.post('/get_answer/')
async def get_answer(query: History) -> dict[str, str]:
    session_id = query.session_id
    _ = await SessionRepository.update_question_count(session_id)

    try:
        user_input = next(
            (msg.content for msg in query.history if msg.role == 'user'), None
        )

        if not user_input:
            raise HTTPException(status_code=400, detail='User message not found')

        answer = get_rag_answer(query.session_id, user_input)

        return {'answer': answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
