from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select
from datetime import datetime
from database.db import async_session
from database.models import User
from aiogram.types import CallbackQuery


router = Router()
@router.message(F.text.startswith("/start"))
async def start_handler(message: Message):
    args = message.text.split()
    referrer_telegram_id = None

    if len(args) > 1:
        try:
            referrer_telegram_id = int(args[1])
        except ValueError:
            referrer_telegram_id = None

    async with async_session() as session:
        user = await session.scalar(
            select(User).where(User.telegram_id == message.from_user.id)
        )

        if not user:
            # Новый пользователь
            new_user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                registered_at=datetime.utcnow(),
                trial_end=None,
                is_subscribed=False,
                referrer_id=referrer_telegram_id
            )
            session.add(new_user)

            # Если пригласивший есть и это не он сам
            if referrer_telegram_id and referrer_telegram_id != message.from_user.id:
                referrer = await session.scalar(
                    select(User).where(User.telegram_id == referrer_telegram_id)
                )
                if referrer:
                    referrer.referral_count = (referrer.referral_count or 0) + 1
                    referrer.activated_referrals = (referrer.activated_referrals or 0) + 1

            await session.commit()

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Бесплатно на 3 дня", callback_data="free_trial")],
        [InlineKeyboardButton(text="📢 DIGDI канал", url="https://t.me/digidichannel")],
        [InlineKeyboardButton(text="💳 Оплатить подписку", callback_data="pay")],
        [InlineKeyboardButton(text="📘 Руководство", callback_data="guide")],
        [InlineKeyboardButton(text="🛠 ТЕХ ПОДДЕРЖКА", callback_data="support")]
    ])

    await message.answer(
        "👋 Добро пожаловать!\nВот что я умею:\n\n"
        "• Бесплатный пробный период на 3 дня\n"
        "• Доступ к DIGDI-каналу\n"
        "• Подписка и ключевые слова\n\n"
        "👇 Выберите нужное:",
        reply_markup=keyboard
    )