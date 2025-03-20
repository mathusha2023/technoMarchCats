from aiogram import Router
from aiogram.types import Message

router = Router()


# самый последний хэндлер, если все остальные были пропущены
@router.message()
async def f(message: Message):
    await message.answer("Нет такого варианта!")
