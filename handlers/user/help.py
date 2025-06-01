# handlers/user/help.py
from aiogram import Router, F
from aiogram.types import Message

router = Router()

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
