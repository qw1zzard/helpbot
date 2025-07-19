import pytest
from src.core.settings import Settings


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv('CHAT_MODEL_NAME', 'test-model')
    monkeypatch.setenv('EMBED_MODEL_NAME', 'test-embed')
    monkeypatch.setenv('DEVICE', 'cpu')
    monkeypatch.setenv('CSV_NAME', 'data.csv')
    monkeypatch.setenv('COLLECTION_NAME', 'helpbot')
    monkeypatch.setenv('QDRANT_URL', 'http://localhost:6333')
    monkeypatch.setenv('SYSTEM_PROMPT', 'System')
    monkeypatch.setenv('CONTEXTUALIZE_Q_SYSTEM_PROMPT', 'Contextualize')
    monkeypatch.setenv('SEARCH_TYPE', 'mmr')
    monkeypatch.setenv('NUM_ANSWERS', '3')
    monkeypatch.setenv('LAMBDA_MULT', '0.8')
    monkeypatch.setenv('TEMPERATURE', '0.2')
    yield


def test_settings_parsing(mock_env):
    settings = Settings()  # type: ignore
    assert settings.chat_model_name == 'test-model'
    assert settings.embed_model_name == 'test-embed'
    assert settings.device == 'cpu'
    assert settings.csv_name == 'data.csv'
    assert settings.collection_name == 'helpbot'
    assert settings.qdrant_url == 'http://localhost:6333'
    assert settings.system_prompt == 'System'
    assert settings.contextualize_q_system_prompt == 'Contextualize'
    assert settings.search_type == 'mmr'
    assert settings.num_answers == 3
    assert settings.lambda_mult == 0.8
    assert settings.temperature == 0.2
