from src.core.model import get_session_history


def test_session_history_persistence():
    session_id = 'test-session'
    history1 = get_session_history(session_id)
    history2 = get_session_history(session_id)
    assert history1 is history2
