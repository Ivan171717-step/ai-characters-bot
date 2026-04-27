import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from bot.characters import CHARACTERS
from bot.config import settings

load_dotenv()

client = AsyncOpenAI(
    api_key=settings.openai_api_key
)


async def generate_ai_response(
    character_id: str,
    user_message: str,
    history: list[dict] | None = None
) -> str:
    character = CHARACTERS.get(character_id)

    if not character:
        return "Сначала выбери персонажа 👆"

    messages = [
        {
            "role": "system",
            "content": str(character["prompt"])
        }
    ]

    if history:
        messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": str(user_message)
        }
    )

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.9,
        messages=messages,
        max_tokens=500
    )

    return response.choices[0].message.content or "Не смог ответить 😢"
