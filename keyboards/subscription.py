from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def subscription_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Тестовый период", callback_data="free_trial")],
        [InlineKeyboardButton(text="💳 Купить подписку", callback_data="choose_currency")],
        [InlineKeyboardButton(text="🤝 Реферальная система", callback_data="referral")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")]
    ])

def currency_choice_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Рубли", callback_data="currency_rub")],
        [InlineKeyboardButton(text="🇰🇬 Сомы", callback_data="currency_kg")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_subscription")]
    ])

def subscription_period_keyboard(currency: str):
    if currency == "rub":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="2 недели - 700₽", callback_data="sub_2w_rub")],
            [InlineKeyboardButton(text="1 месяц - 1400₽", callback_data="sub_1m_rub")],
            [InlineKeyboardButton(text="3 месяца - 4000₽", callback_data="sub_3m_rub")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="choose_currency")]
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="2 недели - 700 сом", callback_data="sub_2w_kg")],
            [InlineKeyboardButton(text="1 месяц - 1400 сом", callback_data="sub_1m_kg")],
            [InlineKeyboardButton(text="3 месяца - 4000 сом", callback_data="sub_3m_kg")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="choose_currency")]
        ])

def referral_keyboard(referral_link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📤 Поделиться ссылкой", switch_inline_query=referral_link)
            ],
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_subscription")
            ]
        ]
    )