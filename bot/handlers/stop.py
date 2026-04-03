from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
import httpx

from bot.utils import get_or_refresh_token
from app.core.config import settings
from bot.storage import user_tokens

router = Router()


@router.message(F.text == "🛑 Стоп")
async def stop_handler(message: Message, state: FSMContext):
    await state.clear()
    token = await get_or_refresh_token(message.from_user.id)

    async with httpx.AsyncClient(timeout=10.0) as client:
        await client.post(
            f"{settings.API_URL}/api/v1/users/me/deactivate",
            headers={"Authorization": f"Bearer {token}"}
        )

    user_tokens.pop(message.from_user.id, None)

    await message.answer(
        "👋 Сповіщення вимкнено. Натисни /start щоб повернутись.",
        reply_markup=ReplyKeyboardRemove()
    )