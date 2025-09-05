import pytest
from src.core.settings import Settings, load_prompt


def test_load_prompt_from_file(tmp_path):
    prompt_file = tmp_path / 'prompt.md'
    prompt_file.write_text('Test prompt content', encoding='utf-8')

    content = load_prompt(str(prompt_file))
    assert content == 'Test prompt content'


def test_load_prompt_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_prompt(str(tmp_path / 'missing.md'))


@pytest.fixture
def env_vars(monkeypatch):
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


def test_settings_parses_env_vars(env_vars):
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
