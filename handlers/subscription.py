from sqlalchemy import select
from database.db import async_session
from database.models import User
from aiogram.types import CallbackQuery
from aiogram import Router, F
from keyboards.subscription import (
    subscription_menu,
    currency_choice_keyboard,
    subscription_period_keyboard,
    referral_keyboard  # добавляем!
)

router = Router()

@router.callback_query(F.data == "pay")
async def show_subscription_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "💳 Подписка действует на все категории. Выберите действие:",
        reply_markup=subscription_menu()
    )


@router.callback_query(F.data == "choose_currency")
async def choose_currency(callback: CallbackQuery):
    await callback.message.edit_text(
        "🌍 Выберите валюту для оплаты:",
        reply_markup=currency_choice_keyboard()
    )


@router.callback_query(F.data.in_({"currency_rub", "currency_kg"}))
async def choose_duration(callback: CallbackQuery):
    currency = "rub" if callback.data == "currency_rub" else "kg"
    await callback.message.edit_text(
        "📆 Выберите период подписки:",
        reply_markup=subscription_period_keyboard(currency)
    )


@router.callback_query(F.data == "back_to_subscription")
async def back_to_subscription(callback: CallbackQuery):
    await show_subscription_menu(callback)


# Обработка выбора подписки (заглушка)
@router.callback_query(F.data.startswith("sub_"))
async def handle_subscription_selection(callback: CallbackQuery):
    await callback.message.edit_text("💸 Платёжная система пока не подключена. Эта часть в разработке.")


@router.callback_query(F.data == "referral")
async def show_referral_info(callback: CallbackQuery):
    user_id = callback.from_user.id
    referral_link = f"https://t.me/didgi_kg_bot?start={user_id}"

    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == user_id))
        total_referrals = user.referral_count if user else 0
        activated_referrals = user.activated_referrals if user else 0
        bonus_months = activated_referrals // 15

    await callback.message.edit_text(
        f"👋 <b>Реферальная система</b>\n\n"
        f"🔗 Ваша персональная ссылка: <code>{referral_link}</code>\n\n"
        f"📊 <b>Статистика:</b>\n"
        f"• Всего рефералов: <b>{total_referrals}</b>\n"
        f"• Активаций: <b>{activated_referrals}</b> из 15\n"
        f"• Бесплатных месяцев: <b>{bonus_months}</b>",
        parse_mode="HTML",
        reply_markup=referral_keyboard(referral_link)
    )
