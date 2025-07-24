import pandas as pd
from src.core.history import ChatHistoryStore
from src.core.model import (
    get_rag_answer,
    populate_if_empty,
    recreate_collection_if_needed,
)


def test_session_history_persistence():
    session_id = 'test'
    h1 = ChatHistoryStore.get_history(session_id)
    h2 = ChatHistoryStore.get_history(session_id)
    assert h1 is h2


def test_add_message():
    session_id = 'test'
    ChatHistoryStore.add_message(session_id, 'user', 'hello')
    assert ChatHistoryStore.get_history(session_id)[-1] == {
        'role': 'user',
        'content': 'hello',
    }


def test_get_rag_answer(mock_qdrant_and_embed, mock_ollama_post):
    answer = get_rag_answer('test-session', 'What is this?')
    assert answer == 'mocked answer'


def test_recreate_collection_if_needed(mock_qdrant_and_embed):
    recreate_collection_if_needed()  # just ensuring no exceptions


def test_populate_if_empty(mock_qdrant_and_embed, monkeypatch):
    pd.DataFrame(
        {
            'id': 1,
            'question': ['What?'],
            'answer': ['Test answer'],
        }
    ).to_csv('data.csv', index=False)
    monkeypatch.setenv('CSV_NAME', str('data.csv'))

    populate_if_empty()
