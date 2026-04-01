import httpx
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from app.core.config import settings

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.API_URL}/api/v1/auth/telegram",
            json={
                "telegram_id": message.from_user.id,
                "username": message.from_user.username,
            }
        )

    if response.status_code == 200:
        data = response.json()
        await message.answer(
            f"Ти успішно авторизований!\n\n"
            f"Твій токен для тестування:\n"
            f"`{data['access_token']}`",
            parse_mode="Markdown"
        )
    else:
        await message.answer("Помилка авторизації")