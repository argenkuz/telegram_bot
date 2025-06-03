from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    """
    Main menu keyboard with all primary bot functions
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Бесплатно на 3 дня", callback_data="free_trial")],
        [InlineKeyboardButton(text="📢 DIGDI канал", url="https://t.me/digidichannel")],
        [InlineKeyboardButton(text="💳 Оплатить подписку", callback_data="pay")],
        [InlineKeyboardButton(text="🔗 Реферальная программа", callback_data="my_referral")],
        [InlineKeyboardButton(text="📘 Руководство", callback_data="guide")],
        [InlineKeyboardButton(text="🛠 ТЕХ ПОДДЕРЖКА", callback_data="support")]
    ])

def get_logged_in_keyboard(username):
    """
    Main menu keyboard for logged in users, with personalized greeting
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"👋 Привет, {username}!", callback_data="profile")],
        [InlineKeyboardButton(text="💳 Мои подписки", callback_data="pay")],
        [InlineKeyboardButton(text="🔗 Реферальная программа", callback_data="my_referral")],
        [InlineKeyboardButton(text="📢 DIGDI канал", url="https://t.me/digidichannel")],
        [InlineKeyboardButton(text="🛠 ТЕХ ПОДДЕРЖКА", callback_data="support")]
    ])

def get_back_to_main_keyboard():
    """
    Simple keyboard with just a back button to main menu
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Главное меню", callback_data="back_to_main")]
    ])