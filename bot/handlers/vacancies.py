from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
import httpx

from app.core.config import settings
from bot.storage import user_tokens
from bot.handlers.keyboards import (
    filters_menu,
    main_menu,
    level_keyboard,
    remote_keyboard,
)
from bot.states import FilterStates
from bot.utils import get_or_refresh_token

router = Router()


@router.message(F.text == "💼 Вакансії")
async def my_vacancy(message: Message):
    token = await get_or_refresh_token(message.from_user.id)
    if not token:
        await message.answer("Спочатку напиши /start")
        return

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"{settings.API_URL}/api/v1/jobs/matched",
            headers={"Authorization": f"Bearer {token}"},
        )

    if response.status_code == 200:
        data = response.json()
        if not data:
            await message.answer("Немає вакансій по твоїх фільтрах.")
            return

        for job in data:
            text = (
                f"💼 {job['title']}\n"
                f"👥 {job['company'] or 'Невідомо'}\n"
                f"📊 {job['level'] or '-'}\n"
                f"🏠 {job['remote_type'] or '-'}\n"
                f"💰 {job['salary_min'] or '-'}\n"
                f"🔗 {job['url']}\n"
            )
            await message.answer(text)
    else:
        await message.answer("Помилка отримання вакансій")
