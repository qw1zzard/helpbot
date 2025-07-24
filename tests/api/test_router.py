import pytest
from fastapi import HTTPException
from src.api.router import extract_user_input
from src.api.schemas import HistoryMessage


def test_extract_user_input_success():
    history = [
        HistoryMessage(role='assistant', content='A'),
        HistoryMessage(role='user', content='B'),
    ]
    assert extract_user_input(history) == 'B'


def test_extract_user_input_raises_if_no_user():
    history = [HistoryMessage(role='assistant', content='Only bot')]
    with pytest.raises(HTTPException) as exc_info:
        extract_user_input(history)
    assert exc_info.value.status_code == 400


def test_get_answer_endpoint(
    client, mock_qdrant_and_embedding, mock_repo_get_add, mock_ollama_response
):
    payload = {
        'session_id': 'test-session',
        'history': [{'role': 'user', 'content': 'Test question'}],
    }
    response = client.post('/api/v1/get_answer/', json=payload)
    assert response.status_code == 200
    assert response.json() == {'answer': 'mocked answer'}
