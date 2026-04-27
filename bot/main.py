import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy import select, desc

from bot.ai_service import generate_ai_response
from bot.characters import get_character_by_button
from bot.database import async_session, engine
from bot.models import Base, User, Message
from bot.config import settings

bot = Bot(token=settings.bot_token)
dp = Dispatcher()

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👩 Анастейша")],
        [KeyboardButton(text="😏 Джейсон")],
        [KeyboardButton(text="🔄 Сменить персонажа")]
    ],
    resize_keyboard=True
)


async def get_or_create_user(telegram_id: int) -> User:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if user:
            return user

        user = User(telegram_id=telegram_id, character=None)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def set_user_character(telegram_id: int, character_id: str):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(telegram_id=telegram_id, character=character_id)
            session.add(user)
        else:
            user.character = character_id

        await session.commit()


async def save_message(telegram_id: int, role: str, content: str):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(telegram_id=telegram_id, character=None)
            session.add(user)
            await session.commit()
            await session.refresh(user)

        message = Message(
            user_id=user.id,
            role=role,
            content=content
        )

        session.add(message)
        await session.commit()

async def get_dialog_history(telegram_id: int, limit: int = 10) -> list[dict]:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            return []

        result = await session.execute(
            select(Message)
            .where(Message.user_id == user.id)
            .order_by(desc(Message.id))
            .limit(limit)
        )

        messages = list(result.scalars().all())
        messages.reverse()

        history = []

        for msg in messages:
            role = "assistant" if msg.role == "bot" else "user"

            history.append({
                "role": role,
                "content": msg.content
            })

        return history


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await get_or_create_user(message.from_user.id)

    await message.answer(
        "Выбери, с кем будешь общаться:",
        reply_markup=keyboard
    )


@dp.message()
async def message_handler(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    user = await get_or_create_user(user_id)

    character_id, character_data = get_character_by_button(text)

    if character_id:
        await set_user_character(user_id, character_id)
        await message.answer(f"Ты выбрал: {character_data['name']} 😏")
        return

    if text == "🔄 Сменить персонажа":
        await set_user_character(user_id, None)
        await message.answer("Окей, выбери нового персонажа 👇")
        return

    if not user.character:
        await message.answer("Сначала выбери персонажа 👆")
        return

    history = await get_dialog_history(user_id)

    await save_message(user_id, "user", text)

    await message.answer("Думаю... 🤔")

    try:
        ai_response = await generate_ai_response(
            user.character,
            text,
            history
        )

        await save_message(user_id, "bot", ai_response)

        await message.answer(ai_response)
    except Exception as e:
        await message.answer("Ошибка AI 😢 Попробуй позже")
        import traceback
        traceback.print_exc()

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
