# handlers/user.py
from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from database.db import async_session
from datetime import datetime, timedelta

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message):
    async with async_session() as session:
        user_in_db = await session.scalar(
            select(User).where(User.telegram_id == message.from_user.id)
        )

        if user_in_db:
            await message.answer("Вы уже зарегистрированы ✅")
            return

        new_user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            registered_at=datetime.utcnow(),
            trial_end=datetime.utcnow() + timedelta(days=3),
            is_subscribed=False,
        )

        session.add(new_user)
        await session.commit()

        await message.answer(
            "👋 Добро пожаловать!\n"
            "Вы получили бесплатный доступ на 3 дня.\n"
            "Я буду присылать вам сообщения по ключевым словам 📩"
        )

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

    @router.message(F.text == "/help")
    async def help_handler(message: Message):
        await message.answer(
            "📖 <b>Помощь</b>\n"
            "/start — запустить бота\n"
            "/status — статус подписки/триала\n"
            "/subscribe — оформить подписку\n"
            "/help — показать эту справку\n\n"
            "Бот будет присылать сообщения из групп, если они содержат ваши ключевые слова 🔍"
        )

    @router.message(F.text == "/subscribe")
    async def subscribe_handler(message: Message):
        await message.answer(
            "💳 Подписка стоит 299₽/мес.\n"
            "Скоро появится кнопка оплаты. Пока это заглушка 🚧"
        )
