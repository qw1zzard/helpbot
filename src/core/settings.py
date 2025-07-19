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

    chat_model_name: str = Field()
    embed_model_name: str = Field()

    device: str = Field()
    temperature: float = Field()

    qdrant_url: str = Field()
    collection_name: str = Field()
    search_type: str = Field()
    num_answers: int = Field()
    lambda_mult: float = Field()

    csv_name: str = Field()

    postgres_host: str = Field()
    postgres_port: int = Field()
    postgres_user: str = Field()
    postgres_password: str = Field()
    postgres_db: str = Field()

    context_prompt: str = load_prompt('prompts/context.md')
    system_prompt: str = load_prompt('prompts/system.md')


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
