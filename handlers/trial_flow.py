from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select
from database.db import async_session
from database.models import User
from datetime import datetime, timedelta

router = Router()

# Шаг 1: Подписка
@router.callback_query(F.data == "free_trial")
async def send_subscription_links(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подписаться на канал 1", url="https://t.me/argen1233")],
            [InlineKeyboardButton(text="Подписаться на канал 2", url="https://t.me/argen12344")],
            [InlineKeyboardButton(text="✅ Я подписался", callback_data="check_subscription")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")]
        ]
    )
    await callback.message.edit_text("📌 Подпишитесь на оба канала и нажмите 'Я подписался'", reply_markup=keyboard)


# Шаг 2: Проверка подписки
@router.callback_query(F.data == "check_subscription")
async def check_subscription(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    try:
        chat1 = await bot.get_chat_member(chat_id="@argen1233", user_id=user_id)
        chat2 = await bot.get_chat_member(chat_id="@argen12344", user_id=user_id)
        subscribed = chat1.status in ["member", "administrator", "creator"] and \
                     chat2.status in ["member", "administrator", "creator"]
    except Exception:
        subscribed = False

    if subscribed:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📂 Выбрать категорию", callback_data="choose_category")],
                [InlineKeyboardButton(text="⬅️ Назад", callback_data="free_trial")]
            ]
        )
        await callback.message.edit_text("✅ Подписка подтверждена!", reply_markup=keyboard)
    else:
        await callback.message.answer("❌ Вы не подписались на все каналы.")


# Шаг 3: Категория
@router.callback_query(F.data == "choose_category")
async def choose_category(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎉 Активировать пробный период", callback_data="activate_trial")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="check_subscription")]
        ]
    )
    await callback.message.edit_text("🔎 Категория выбрана.\nТеперь активируйте триал:", reply_markup=keyboard)


# Шаг 4: Активация триала

@router.callback_query(F.data == "activate_trial")
async def activate_trial(callback: CallbackQuery):
    async with async_session() as session:
        user = await session.scalar(
            select(User).where(User.telegram_id == callback.from_user.id)
        )

        if not user:
            await callback.message.answer("❌ Пользователь не найден.")
            return

        now = datetime.utcnow()

        # Преобразуем строку в datetime, если необходимо
        trial_end = user.trial_end
        if isinstance(trial_end, str):
            try:
                trial_end = datetime.fromisoformat(trial_end)
            except ValueError:
                trial_end = None

        # Если триал активен — не обновляем
        if trial_end and trial_end > now:
            await callback.message.edit_text(
                f"ℹ️ У вас уже активирован триал до:\n<b>{trial_end.strftime('%Y-%m-%d %H:%M:%S')}</b>",
                parse_mode="HTML"
            )
        else:
            user.trial_end = now + timedelta(days=3)
            await session.commit()
            await callback.message.edit_text("✅ Триал активирован на 3 дня! 🎉")



