from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_qdrant():
    with (
        patch(
            'src.core.model.QdrantClient.get_collections',
            return_value=type('C', (), {'collections': []})(),
        ),
        patch('src.core.model.QdrantClient.recreate_collection', return_value=None),
        patch(
            'src.core.model.QdrantClient.count',
            return_value=type('C', (), {'count': 1})(),
        ),
    ):
        yield


@pytest.fixture
def mock_embed():
    with patch(
        'src.core.model.HuggingFaceEmbeddings.embed_query', return_value=[0.0] * 384
    ):
        yield


@pytest.fixture
def mock_ollama():
    with patch('src.core.model.ChatOllama'):
        yield


@pytest.fixture
def mock_repo_methods():
    with (
        patch(
            'src.db.repository.SessionRepository._get_last_session',
            new_callable=AsyncMock,
        ) as mock_get,
        patch(
            'src.db.repository.SessionRepository._add_session', new_callable=AsyncMock
        ) as mock_add,
    ):
        yield mock_get, mock_add


@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)
