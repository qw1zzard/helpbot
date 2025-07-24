from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import numpy as np
import pytest
import streamlit as st
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def mock_qdrant():
    with patch('src.core.model.qdrant_client') as mock_qdrant:
        mock_qdrant.get_collections.return_value.collections = []
        mock_qdrant.count.return_value.count = 0
        yield mock_qdrant


@pytest.fixture
def mock_embedding():
    with patch('src.core.model.embedding_model') as mock_embed:
        mock_embed.encode.return_value = np.ones(384) * 0.1
        yield mock_embed


@pytest.fixture
def mock_qdrant_and_embedding(mock_qdrant, mock_embedding):
    yield mock_qdrant, mock_embedding


@pytest.fixture
def mock_ollama_response():
    with patch('src.core.model.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'message': {'content': 'mocked answer'}
        }
        yield mock_post


@pytest.fixture
def mock_requests_post_success():
    with patch('src.core.model.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'message': {'content': 'mocked answer'}
        }
        yield mock_post


@pytest.fixture
def mock_repo_get_add():
    mock_get = AsyncMock()
    mock_get.return_value = MagicMock(timestamp=datetime.now())

    mock_add = AsyncMock()

    with (
        patch('src.db.repository.SessionRepository._get_last_session', mock_get),
        patch('src.db.repository.SessionRepository._add_session', mock_add),
    ):
        yield mock_get, mock_add


@pytest.fixture
def clear_streamlit_state():
    st.session_state.clear()
