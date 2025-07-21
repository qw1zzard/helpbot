from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def load_prompt(path: str) -> str:
    """Load a prompt from a .md or .txt file."""
    prompt_path = Path(path)

    if not prompt_path.is_file():
        raise FileNotFoundError(f'Prompt file not found: {prompt_path.resolve()}')

    return prompt_path.read_text(encoding='utf-8').strip()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    chat_model_name: str = Field(default='gemma3:1b')
    embed_model_name: str = Field(default='ai-forever/ru-en-RoSBERTa')

    device: str = Field(default='cpu')
    temperature: float = Field(default=0.5)

    qdrant_url: str = Field(default='http://qdrant:6333')
    collection_name: str = Field(default='helpbot')
    search_type: str = Field(default='mrr')
    num_answers: int = Field(default=5)
    lambda_mult: float = Field(default=0.25)

    csv_name: str = Field(default='data.csv')

    postgres_host: str = Field(default='helpbot')
    postgres_port: int = Field(default=5432)
    postgres_user: str = Field(default='helpbot')
    postgres_password: str = Field(default='helpbot')
    postgres_db: str = Field(default='helpbot')

    telegram_token: str = Field(default='dummy-token')

    context_prompt: str = load_prompt('prompts/context.md')
    system_prompt: str = load_prompt('prompts/system.md')


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
