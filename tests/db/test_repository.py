from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch

import pytest
from src.db.repository import SessionRepository


@pytest.mark.asyncio
@patch('src.db.repository.SessionRepository._get_last_session', new_callable=AsyncMock)
@patch('src.db.repository.SessionRepository._add_session', new_callable=AsyncMock)
async def test_new_session(mock_add, mock_get):
    mock_get.return_value = None
    count = await SessionRepository.update_question_count('new-session')
    assert count == 1
    mock_add.assert_awaited_once()


@pytest.mark.asyncio
@patch('src.db.repository.SessionRepository._get_last_session', new_callable=AsyncMock)
@patch('src.db.repository.SessionRepository._add_session', new_callable=AsyncMock)
async def test_same_session_in_time(mock_add, mock_get):
    mock_get.return_value = type(
        'S', (), {'timestamp': datetime.now(), 'question_count': 1}
    )()
    count = await SessionRepository.update_question_count('existing')
    assert count == 2  # 1 % 2 + 1
    mock_add.assert_awaited_once()


@pytest.mark.asyncio
@patch('src.db.repository.SessionRepository._get_last_session', new_callable=AsyncMock)
@patch('src.db.repository.SessionRepository._add_session', new_callable=AsyncMock)
async def test_session_expired(mock_add, mock_get):
    mock_get.return_value = type(
        'S', (), {'timestamp': datetime.now() - timedelta(hours=1)}
    )()
    count = await SessionRepository.update_question_count('expired')
    assert count == 1
    mock_add.assert_awaited_once()
