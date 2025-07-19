from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory


class ChatHistoryStore:
    _instance = None
    _store: dict[str, ChatMessageHistory] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatHistoryStore, cls).__new__(cls)
        return cls._instance

    def get_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self._store:
            self._store[session_id] = ChatMessageHistory()
        return self._store[session_id]
