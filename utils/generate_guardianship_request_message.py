from aiogram.types import Message

from keyboards import delete_request_keyboard


async def generate_guardianship_request_message(request, message: Message):
    user = request.user
    animal = request.animal

    text = f"""Пользователь {user.first_name} хочет взять котика {animal.name} (ID={animal.id}). Свяжитесь с пользователем, чтобы обсудить детали.
tg: @{user.username}"""

    await message.answer(text, reply_markup=delete_request_keyboard(request.id))

