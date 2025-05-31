# bot.py
import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.db import init_db
from handlers import user  # импортируем наш хендлер

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(user.router)  # регистрируем команды

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
