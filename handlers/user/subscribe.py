# handlers/user/subscription.py
from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "/subscribe")
async def subscribe_handler(message: Message):
    await message.answer(
        "💳 Подписка стоит 299₽/мес.\n"
        "Скоро появится кнопка оплаты. Пока это заглушка 🚧"
    )
