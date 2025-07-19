from datetime import datetime, timedelta

import pytest
from src.db.repository import SessionRepository


@pytest.mark.asyncio
async def test_new_session(mock_repo_methods, mock_session):
    mock_get, mock_add = mock_repo_methods
    mock_get.return_value = None
    count = await SessionRepository.update_question_count('new-session', mock_session)
    assert count == 1
    mock_add.assert_awaited_once()


@pytest.mark.asyncio
async def test_same_session_in_time(mock_repo_methods, mock_session):
    mock_get, mock_add = mock_repo_methods
    mock_get.return_value = type(
        'S', (), {'timestamp': datetime.now(), 'question_count': 1}
    )()
    count = await SessionRepository.update_question_count('existing', mock_session)
    assert count == 2  # 1 % 2 + 1
    mock_add.assert_awaited_once()


@pytest.mark.asyncio
async def test_session_expired(mock_repo_methods, mock_session):
    mock_get, mock_add = mock_repo_methods
    mock_get.return_value = type(
        'S', (), {'timestamp': datetime.now() - timedelta(hours=1)}
    )()
    count = await SessionRepository.update_question_count('expired', mock_session)
    assert count == 1
    mock_add.assert_awaited_once()
