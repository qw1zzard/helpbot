import pytest
from pydantic import ValidationError
from src.api.schemas import History, HistoryMessage


def test_history_message_valid():
    msg = HistoryMessage(role='user', content='Hello')
    assert msg.role == 'user'
    assert msg.content == 'Hello'


def test_history_message_invalid_role():
    with pytest.raises(ValidationError):
        HistoryMessage(content='Hello')  # type: ignore


def test_history_valid():
    h = History(
        session_id='sess1',
        history=[
            HistoryMessage(
                role='user',
                content='Hi',
            ),
        ],
    )
    assert h.session_id == 'sess1'
    assert len(h.history) == 1


def test_history_invalid_missing_session_id():
    with pytest.raises(ValidationError):
        History(history=[])  # type: ignore
