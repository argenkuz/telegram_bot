# bot.py
import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.db import init_db
from handlers import user  # импортируем наш хендлер
from handlers import trial_flow
from handlers import guide
from handlers import support_callback
from handlers import subscription
from handlers.user.referral import router as referral_router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(user.routers)  # регистрируем команды
dp.include_router(trial_flow.router)
dp.include_router(guide.router)
dp.include_router(support_callback.router)
dp.include_router(subscription.router)
dp.include_router(referral_router)
async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
