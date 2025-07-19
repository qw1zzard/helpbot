from unittest.mock import patch

from src.core.model import (
    create_conversational_rag_chain,
    get_rag_answer,
    get_session_history,
)


def test_session_history_persistence():
    session_id = 'test-session'
    history1 = get_session_history(session_id)
    history2 = get_session_history(session_id)
    assert history1 is history2


def test_create_rag_chain_returns_chain(mock_qdrant, mock_embed, mock_ollama):
    chain = create_conversational_rag_chain()
    assert hasattr(chain, 'invoke')


@patch('src.core.model.conversational_rag_chain')
def test_get_rag_answer_output_type(mock_chain):
    mock_chain.invoke.return_value = {'answer': '42'}
    response = get_rag_answer('session-id', "What's the answer?")
    assert isinstance(response, str)
    assert response == '42'
