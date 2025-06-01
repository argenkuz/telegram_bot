from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.callback_query(F.data == "support")
async def support_callback(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back_to_start")]
        ]
    )

    await callback.message.edit_text(
        "<b>Контакты для связи:</b>\n\n"
        "▪️ Администратор – <a href='https://t.me/Art_666999'>@Art_666999</a>\n"
        "▫️ Сотрудничество, реклама, подписки, другие вопросы.\n\n"
        "▪️ Менеджер – <a href='https://t.me/yongbokkii'>@yongbokkii</a>\n"
        "▫️ Помощь, подписки, другие вопросы.\n\n"
        "▪️ Разработчик – <a href='https://t.me/iredoff'>@iredoff</a>\n"
        "▫️ Тех. проблемы.\n\n"
        "<b>Обратите внимание:</b>\n"
        "Если вы уже написали одному из сотрудников, но он не в сети — дождитесь ответа.\n"
        "Не пишите тот же вопрос другому, это создаёт путаницу и задержки.",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
