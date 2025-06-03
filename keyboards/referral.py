from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def referral_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Моя статистика", callback_data="referral_stats")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
    ])

def referral_stats_keyboard(has_rewards=False):
    buttons = [
        [InlineKeyboardButton(text="🔗 Моя ссылка", callback_data="my_referral")]
    ]
    
    if has_rewards:
        buttons.append([InlineKeyboardButton(text="💰 Использовать награду", callback_data="use_reward")])
    else:
        buttons.append([InlineKeyboardButton(text="💰 Использовать награду", callback_data="no_rewards")])
        
    buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)