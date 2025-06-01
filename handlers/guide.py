from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.callback_query(F.data == "guide")
async def guide(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back_to_start")]
        ]
    )

    await callback.message.edit_text(
        "📘 <b>Руководство по использованию бота</b>\n\n"
        "👋 Этот бот помогает вам отслеживать сообщения из Telegram-групп по ключевым словам.\n\n"
        "🔍 Вы можете указать интересующие вас темы, и бот будет автоматически присылать совпадения.\n\n"
        "🧪 Доступен бесплатный пробный период — 3 дня.\n"
        "💳 Есть платная подписка для постоянного доступа.\n\n"
        "🤝 Мы создали этот бот, чтобы сэкономить ваше время и помочь следить за важным в потоке информации.\n"
        "📈 Над проектом работают энтузиасты в области аналитики и автоматизации.\n\n"
        "💬 Если возникнут вопросы — нажмите «Техподдержка» ниже.",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
