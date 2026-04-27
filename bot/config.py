import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    database_url: str = "sqlite+aiosqlite:///./bot.db"


def _get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            f"Create a .env file and set {name}."
        )
    return value


settings = Settings(
    bot_token=_get_required_env("BOT_TOKEN"),
    openai_api_key=_get_required_env("OPENAI_API_KEY"),
    openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    database_url=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bot.db"),
)
