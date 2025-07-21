from unittest.mock import MagicMock, patch

from src.core.history import ChatHistoryStore
from src.core.model import get_rag_answer


def test_session_history_persistence():
    session_id = 'test-session'
    history_store = ChatHistoryStore()
    history_1 = history_store.get_history(session_id)
    history_2 = history_store.get_history(session_id)
    assert history_1 is history_2


@patch('src.core.model.embedding_model')
@patch('src.core.model.qdrant_client')
@patch('src.core.model.requests.post')
def test_get_rag_answer_output(mock_post, mock_qdrant, mock_embed):
    mock_embed.encode.return_value = [0.1] * 384

    mock_qdrant.search.return_value = [
        MagicMock(payload={'answer': 'Answer 1'}),
        MagicMock(payload={'answer': 'Answer 2'}),
    ]

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {'message': {'content': '42'}}

    response = get_rag_answer('test-session', "What's the answer?")
    assert response == '42'

    history = ChatHistoryStore().get_history('test-session')
    assert history[-1]['role'] == 'assistant'
    assert history[-1]['content'] == '42'
