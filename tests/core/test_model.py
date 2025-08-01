from unittest.mock import patch

import pandas as pd
from src.core.history import ChatHistoryStore
from src.core.model import (
    fill_collection,
    get_rag_answer,
    recreate_collection,
)
from src.core.settings import Settings


def test_session_history_is_singleton():
    h1 = ChatHistoryStore.get_history('test')
    h2 = ChatHistoryStore.get_history('test')
    assert h1 is h2


def test_add_message_to_history():
    session_id = 'test'
    ChatHistoryStore.add_message(session_id, 'user', 'hello')
    last_message = ChatHistoryStore.get_history(session_id)[-1]
    assert last_message == {'role': 'user', 'content': 'hello'}


def test_get_rag_answer_returns_mock(mock_qdrant, mock_embedding, mock_requests_post):
    answer = get_rag_answer('test-session', 'What is this?')
    assert answer == 'mocked answer'


def test_recreate_collection(mock_qdrant, mock_embedding):
    recreate_collection()


def test_populate_reads_csv(tmp_path, monkeypatch, mock_qdrant, mock_embedding):
    df = pd.DataFrame({'id': [1], 'question': ['What?'], 'answer': ['Test answer']})

    test_csv = tmp_path / 'data.csv'
    df.to_csv(test_csv, index=False)

    new_settings = Settings.model_construct(
        _env_file=None, _env_file_encoding=None, csv_name=str(test_csv)
    )

    with patch('src.core.model.settings', new_settings):
        fill_collection()
