from aiogram.types import Message
from data.db_session import create_session
from data.animals import Animal
from utils.get_text_gender import get_text_gender
import keyboards

# сообщение списка животных для админа
async def generate_animals_admin_list(message: Message):
    session = create_session()

    animals = session.query(Animal).order_by(Animal.id).all()

    if animals:
        text = ""
        for animal in animals:
            s = f"{animal.id}. {animal.name}, {get_text_gender(animal.gender)}, {animal.get_age()[0]} лет\n"
            text += s
    else:
        text = "Пока что в базе данных нет животных:/"

    await message.answer(text, reply_markup=keyboards.close_animals_admin_list_keyboard())
