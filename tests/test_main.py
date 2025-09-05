from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI
from src.main import lifespan


@pytest.mark.asyncio
async def test_lifespan_starts_components():
    mock_create_tables = AsyncMock()
    mock_recreate = MagicMock()
    mock_populate = MagicMock()

    with (
        patch('src.main.create_tables', mock_create_tables),
        patch('src.main.recreate_collection', mock_recreate),
        patch('src.main.fill_collection', mock_populate),
    ):
        async with lifespan(FastAPI()):
            pass

    mock_create_tables.assert_awaited_once()
    mock_recreate.assert_called_once()
    mock_populate.assert_called_once()


def test_healthcheck(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}
