import pytest
from fastapi import HTTPException
from src.api.router import extract_user_input
from src.api.schemas import HistoryMessage


def test_extract_user_input_success():
    history = [
        HistoryMessage(role='assistant', content='Hello'),
        HistoryMessage(role='user', content='Hi'),
    ]
    assert extract_user_input(history) == 'Hi'


def test_extract_user_input_fail():
    history = [HistoryMessage(role='assistant', content='Only bot')]
    with pytest.raises(HTTPException) as e:
        extract_user_input(history)
    assert e.value.status_code == 400


def test_get_answer_endpoint(
    client, mock_qdrant_and_embed, mock_repo_methods, mock_ollama_post
):
    response = client.post(
        '/api/v1/get_answer/',
        json={
            'session_id': 'test-session',
            'history': [{'role': 'user', 'content': 'Test question'}],
        },
    )
    assert response.status_code == 200
    assert response.json() == {'answer': 'mocked answer'}
