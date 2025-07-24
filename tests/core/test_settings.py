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
    monkeypatch.setenv('SYSTEM_PROMPT', 'system prompt')
    monkeypatch.setenv('CONTEXT_PROMPT', 'context prompt')
    monkeypatch.setenv('SEARCH_TYPE', 'mmr')
    monkeypatch.setenv('NUM_ANSWERS', '3')
    monkeypatch.setenv('LAMBDA_MULT', '0.8')
    monkeypatch.setenv('TEMPERATURE', '0.2')
    yield


def test_settings_parsing(mock_env):
    settings = Settings()
    assert settings.chat_model_name == 'test-model'
    assert settings.embed_model_name == 'test-embed'
    assert settings.device == 'cpu'
    assert settings.csv_name == 'data.csv'
    assert settings.collection_name == 'helpbot'
    assert settings.qdrant_url == 'http://localhost:6333'
    assert settings.system_prompt == 'system prompt'
    assert settings.context_prompt == 'context prompt'
    assert settings.search_type == 'mmr'
    assert settings.num_answers == 3
    assert settings.lambda_mult == 0.8
    assert settings.temperature == 0.2
