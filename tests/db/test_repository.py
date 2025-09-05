from datetime import datetime, timedelta

import pytest
from src.db.repository import SessionRepository


@pytest.mark.asyncio
async def test_adds_new_session(mock_repo_get_add, mock_session):
    mock_get, mock_add = mock_repo_get_add
    mock_get.return_value = None
    await SessionRepository.update_session('session1', mock_session)
    mock_add.assert_awaited_once()


@pytest.mark.asyncio
async def test_skips_recent_session(mock_repo_get_add, mock_session):
    mock_get, mock_add = mock_repo_get_add
    mock_get.return_value.timestamp = datetime.now()
    await SessionRepository.update_session('session2', mock_session)
    mock_add.assert_not_awaited()


@pytest.mark.asyncio
async def test_adds_if_session_expired(mock_repo_get_add, mock_session):
    mock_get, mock_add = mock_repo_get_add
    mock_get.return_value.timestamp = datetime.now() - timedelta(hours=1)
    await SessionRepository.update_session('session3', mock_session)
    mock_add.assert_awaited_once()
