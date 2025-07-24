import pandas as pd
from src.core.history import ChatHistoryStore
from src.core.model import (
    get_rag_answer,
    populate_if_empty,
    recreate_collection_if_needed,
)


def test_session_history_is_singleton():
    h1 = ChatHistoryStore.get_history('test')
    h2 = ChatHistoryStore.get_history('test')
    assert h1 is h2


def test_add_message_to_history():
    session_id = 'test'
    ChatHistoryStore.add_message(session_id, 'user', 'hello')
    last_message = ChatHistoryStore.get_history(session_id)[-1]
    assert last_message == {'role': 'user', 'content': 'hello'}


def test_get_rag_answer_returns_mock(
    mock_qdrant, mock_embedding, mock_requests_post_success
):
    answer = get_rag_answer('test-session', 'What is this?')
    assert answer == 'mocked answer'


def test_recreate_collection_if_needed(mock_qdrant, mock_embedding):
    recreate_collection_if_needed()


def test_populate_if_empty_reads_csv(
    tmp_path, monkeypatch, mock_qdrant, mock_embedding
):
    df = pd.DataFrame({'id': [1], 'question': ['What?'], 'answer': ['Test answer']})

    test_csv = tmp_path / 'data.csv'
    df.to_csv(test_csv, index=False)

    monkeypatch.setenv('CSV_NAME', str(test_csv))

    populate_if_empty()
