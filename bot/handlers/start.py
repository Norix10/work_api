import httpx
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


from app.core.config import settings
from bot.storage import user_tokens
from bot.handlers.keyboards import main_menu
from bot.utils import get_or_refresh_token

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{settings.API_URL}/api/v1/auth/telegram",
            json={
                "telegram_id": message.from_user.id,
                "username": message.from_user.username,
            },
        )

    if response.status_code == 200:
        data = response.json()
        await message.answer(
            f"Ти успішно авторизований!\n",
            parse_mode="Markdown",
        )
        user_tokens[message.from_user.id] = data["access_token"]
    else:
        await message.answer("Помилка авторизації")

    await message.answer("Головне меню:", reply_markup=main_menu)


@router.message(Command("token"))
async def token_handler(message: Message):
    token = await get_or_refresh_token(message.from_user.id)
    await message.answer(f"Твій токен: `{token}`", parse_mode="Markdown")

