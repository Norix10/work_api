import asyncio
from aiogram import Bot, Dispatcher, types

from app.core.config import settings
from bot.handlers import start, filters, vacancies, stop


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(start.router)
    dp.include_router(filters.router)
    dp.include_router(vacancies.router)
    dp.include_router(stop.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
