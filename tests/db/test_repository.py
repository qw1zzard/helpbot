from datetime import datetime, timedelta

import pytest
from src.db.repository import SessionRepository


@pytest.mark.asyncio
async def test_new_session(mock_repo_methods, mock_session):
    mock_get, mock_add = mock_repo_methods
    mock_get.return_value = None
    await SessionRepository.update_session('new-session', mock_session)
    mock_add.assert_awaited_once()


@pytest.mark.asyncio
async def test_same_session_in_time(mock_repo_methods, mock_session):
    mock_get, mock_add = mock_repo_methods
    mock_get.return_value = type('S', (), {'timestamp': datetime.now()})()
    await SessionRepository.update_session('existing', mock_session)
    mock_add.assert_not_awaited()


@pytest.mark.asyncio
async def test_session_expired(mock_repo_methods, mock_session):
    mock_get, mock_add = mock_repo_methods
    mock_get.return_value = type(
        'S', (), {'timestamp': datetime.now() - timedelta(hours=1)}
    )()
    await SessionRepository.update_session('expired', mock_session)
    mock_add.assert_awaited_once()
