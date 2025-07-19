from unittest.mock import MagicMock, patch

from src.core.history import ChatHistoryStore
from src.core.model import create_conversational_rag_chain, get_rag_answer


def test_session_history_persistence():
    session_id = 'test-session'
    history_store = ChatHistoryStore()
    history_1 = history_store.get_history(session_id)
    history_2 = history_store.get_history(session_id)
    assert history_1 is history_2


def test_create_rag_chain(mock_qdrant, mock_embed, mock_ollama):
    chain = create_conversational_rag_chain()
    assert hasattr(chain, 'invoke')


@patch('src.core.model.get_chain')
def test_get_rag_answer_output(mock_get_chain):
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {'answer': '42'}
    mock_get_chain.return_value = mock_chain

    response = get_rag_answer('session-id', "What's the answer?")
    assert response == '42'
