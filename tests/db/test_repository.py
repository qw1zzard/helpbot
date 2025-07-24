from datetime import datetime, timedelta

import pytest
from src.db.repository import SessionRepository


@pytest.mark.asyncio
async def test_new_session(mock_repo_methods, mock_session):
    mock_get, mock_add = mock_repo_methods
    mock_get.return_value = None
    await SessionRepository.update_session('session1', mock_session)
    mock_add.assert_awaited_once()


@pytest.mark.asyncio
async def test_recent_session_no_add(mock_repo_methods, mock_session):
    mock_get, mock_add = mock_repo_methods
    mock_get.return_value = type('M', (), {'timestamp': datetime.now()})()
    await SessionRepository.update_session('session2', mock_session)
    mock_add.assert_not_awaited()


@pytest.mark.asyncio
async def test_expired_session_add(mock_repo_methods, mock_session):
    mock_get, mock_add = mock_repo_methods
    mock_get.return_value = type(
        'M', (), {'timestamp': datetime.now() - timedelta(hours=1)}
    )()
    await SessionRepository.update_session('session3', mock_session)
    mock_add.assert_awaited_once()
