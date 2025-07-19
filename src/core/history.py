from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory


class ChatHistoryStore:
    _store: dict[str, ChatMessageHistory] = {}

    @classmethod
    def get_history(cls, session_id: str) -> BaseChatMessageHistory:
        if session_id not in cls._store:
            cls._store[session_id] = ChatMessageHistory()

        return cls._store[session_id]
