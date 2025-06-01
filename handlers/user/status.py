# handlers/user/status.py
from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select
from datetime import datetime
from database.db import async_session
from database.models import User

router = Router()

@router.message(F.text == "/status")
async def status_handler(message: Message):
    async with async_session() as session:
        user = await session.scalar(
            select(User).where(User.telegram_id == message.from_user.id)
        )

        if not user:
            await message.answer("Вы ещё не зарегистрированы. Введите /start.")
            return

        now = datetime.utcnow()
        if user.is_subscribed and user.subscription_end and user.subscription_end > now:
            days_left = (user.subscription_end - now).days
            await message.answer(f"🟢 У вас активная подписка.\nОсталось дней: {days_left}")
        elif user.trial_end and user.trial_end > now:
            days_left = (user.trial_end - now).days
            await message.answer(f"🟡 У вас активен триал.\nОсталось дней: {days_left}")
        else:
            await message.answer("🔴 У вас нет активной подписки.\nВведите /subscribe для оформления.")

