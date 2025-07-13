from pydantic import BaseModel


class HistoryMessage(BaseModel):
    role: str  # in ('user', 'assistant')
    content: str


class History(BaseModel):
    session_id: str
    history: list[HistoryMessage]
