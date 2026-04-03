from email.mime import message

from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardRemove,
)
from aiogram import Router, F, filters
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
from bot.states import FilterStates, LEVEL_MAP, REMOTE_MAP
from bot.utils import get_or_refresh_token


router = Router()


@router.message(F.text == "🎛 Мої фільтри")
async def my_filters(message: Message):
    token = await get_or_refresh_token(message.from_user.id)
    if not token:
        await message.answer("Спочатку напиши /start")
        return

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{settings.API_URL}/api/v1/filters/",
            headers={"Authorization": f"Bearer {token}"},
        )
    if response.status_code == 200:
        await message.answer("Управління фільтрами:", reply_markup=filters_menu)
        data = response.json()
        if not data:
            await message.answer("У тебе немає фільтрів.")
            return

        text = "🎛 Твої фільтри:\n\n"
        for i, f in enumerate(data, 1):
            text += f"#{i}\n"
            text += f"📌 Технології: {', '.join(f['technologies'])}\n"
            text += f"📊 Рівень: {f['level']}\n"
            text += f"💰 Мінімальна зарплата: {f['salary_min']}\n"
            text += f"🏠 Формат: {f['remote_type']}\n\n"

        await message.answer(text)
    else:
        await message.answer("Помилка отримання фільтрів")


@router.message(F.text == "➕ Створити")
async def add_filter_start(message: Message, state: FSMContext):
    await message.answer(
        "Введи технології через кому:\nНаприклад: Python, FastAPI, Django",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(FilterStates.waiting_technologies)


@router.message(FilterStates.waiting_technologies)
async def add_filter_technologies(message: Message, state: FSMContext):
    await state.update_data(technologies=message.text.split(", "))
    await message.answer("Який рівень?", reply_markup=level_keyboard)
    await state.set_state(FilterStates.waiting_level)


@router.message(FilterStates.waiting_level)
async def add_filter_level(message: Message, state: FSMContext):
    await state.update_data(level=LEVEL_MAP.get(message.text, "any"))
    await message.answer("Який формат роботи?", reply_markup=remote_keyboard)
    await state.set_state(FilterStates.waiting_remote)


@router.message(FilterStates.waiting_remote)
async def add_filter_remote(message: Message, state: FSMContext):
    await state.update_data(remote_type=REMOTE_MAP.get(message.text, "any"))
    await message.answer(
        "Який мінімальний рівень зарплати?",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(FilterStates.waiting_salary)


@router.message(FilterStates.waiting_salary)
async def add_filter_salary(message: Message, state: FSMContext):
    await state.update_data(
        salary_min=int(message.text) if message.text.isdigit() else 0
    )
    data = await state.get_data()
    await state.clear()


    token = await get_or_refresh_token(message.from_user.id)
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            f"{settings.API_URL}/api/v1/filters/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "technologies": data["technologies"],
                "level": data["level"],
                "remote_type": data["remote_type"],
                "salary_min": data.get("salary_min", 0),
            },
        )

    if response.status_code == 201:
        await message.answer("✅ Фільтр створено!", reply_markup=main_menu)
    else:
        await message.answer("❌ Помилка створення фільтру", reply_markup=filters_menu)


@router.callback_query(F.data.startswith("delete_filter:"))
async def delete_filter_callback(callback: CallbackQuery):
    filter_id = callback.data.split(":")[1]
    token = await get_or_refresh_token(callback.from_user.id)
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.delete(
            f"{settings.API_URL}/api/v1/filters/{filter_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
    if response.status_code == 204:
        await callback.message.answer("✅ Фільтр видалено!", reply_markup=filters_menu)
    else:
        await callback.message.answer(
            "❌ Помилка видалення фільтру", reply_markup=filters_menu
        )

    await callback.answer()


@router.message(F.text == "🗑 Видалити")
async def delete_filter_start(message: Message):
    token = await get_or_refresh_token(message.from_user.id)

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"{settings.API_URL}/api/v1/filters/",
            headers={"Authorization": f"Bearer {token}"},
        )

    if response.status_code != 200:
        await message.answer("Помилка отримання фільтрів")
        return

    data = response.json()
    if not data:
        await message.answer("У тебе немає фільтрів.")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"#{i} {', '.join(f['technologies'])} - {f['level']}",
                    callback_data=f"delete_filter:{f['id']}",
                )
            ]
            for i, f in enumerate(data, 1)
        ]
    )

    await message.answer("Який фільтр видалити?", reply_markup=keyboard)


@router.message(F.text == "⬅️ Назад")
async def back_handler(message: Message):
    await message.answer("Головне меню:", reply_markup=main_menu)
