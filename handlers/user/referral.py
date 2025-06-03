from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from sqlalchemy import select
from database.db import async_session
from database.models import User
from utils.referral_utils import generate_progress_bar, get_referral_link
from keyboards.referral import referral_main_keyboard, referral_stats_keyboard

router = Router()

@router.callback_query(F.data == "my_referral")
async def show_referral_link(callback: CallbackQuery):
    user_id = callback.from_user.id
    referral_link = await get_referral_link(callback.bot, user_id)
    
    await callback.message.edit_text(
        f"🔗 Ваша реферальная ссылка:\n\n`{referral_link}`\n\n"
        f"Поделитесь ею с друзьями! За каждые 15 привлеченных пользователей "
        f"вы получаете 1 месяц подписки бесплатно!",
        reply_markup=referral_main_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "referral_stats")
async def show_referral_stats(callback: CallbackQuery):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == callback.from_user.id))
        if not user:
            await callback.answer("Пользователь не найден")
            return
            
        total_referrals = user.referral_count or 0
        active_referrals = user.activated_referrals or 0
        rewards_earned = user.referral_rewards_earned or 0
        rewards_used = user.referral_rewards_used or 0
        rewards_available = rewards_earned - rewards_used
        
        progress_percentage = (active_referrals % 15) / 15 * 100 if active_referrals > 0 else 0
        progress_bar = generate_progress_bar(progress_percentage)
        
        await callback.message.edit_text(
            f"📊 *Ваша реферальная статистика:*\n\n"
            f"👥 Всего приглашено: {total_referrals}\n"
            f"✅ Активировано: {active_referrals}\n"
            f"🎁 Заработано наград: {rewards_earned}\n"
            f"🔄 Использовано наград: {rewards_used}\n"
            f"💎 Доступно наград: {rewards_available}\n\n"
            f"До следующей награды: {active_referrals % 15}/15\n{progress_bar}",
            reply_markup=referral_stats_keyboard(has_rewards=rewards_available > 0),
            parse_mode="Markdown"
        )

@router.message(F.text == "/referral")
async def referral_command(message: Message):
    user_id = message.from_user.id
    referral_link = await get_referral_link(message.bot, user_id)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Моя статистика", callback_data="referral_stats")]
    ])
    
    await message.answer(
        f"🔗 *Ваша реферальная ссылка:*\n\n`{referral_link}`\n\n"
        f"Поделитесь ею с друзьями! За каждые 15 привлеченных пользователей "
        f"вы получаете 1 месяц подписки бесплатно!",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )