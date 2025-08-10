class ChatHistoryStore:
    _store: dict[str, list[dict[str, str]]] = {}

    @classmethod
    def get_history(cls, session_id: str) -> list[dict[str, str]]:
        return cls._store.setdefault(session_id, [])

    @classmethod
    def add_message(cls, session_id: str, role: str, content: str) -> None:
        cls.get_history(session_id).append({'role': role, 'content': content})
