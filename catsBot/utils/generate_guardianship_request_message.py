from aiogram.types import Message

from keyboards import delete_request_keyboard


# генерация заявки об опекунстве для админа
async def generate_guardianship_request_message(request, message: Message):
    user = request.user
    animal = request.animal

    text = f"""Пользователь: {user.firstName}
Котик: {animal.name} (ID={animal.id}) 
Свяжитесь с пользователем, чтобы обсудить детали.
tg: @{user.username}"""

    image = animal.images[0].image

    await message.answer_photo(image, caption=text, reply_markup=delete_request_keyboard(request.id))

