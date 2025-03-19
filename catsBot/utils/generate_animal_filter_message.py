from aiogram.types import Message
import keyboards
from utils.get_text_gender import get_text_gender

# сообщение фильтра при просмотре животных
async def generate_animal_filter_message(message: Message, animal_filter, edit=False, add_keyboard=True):
    text = f"""Настройте свой кошачий фильтр! Сейчас он выглядит так:
        
Пол питомца: {get_text_gender(animal_filter.gender)}
        
➖➖➖➖➖➖➖➖➖➖➖
        
Возраст питомца: от {animal_filter.minAge} до {animal_filter.maxAge} лет
        
➖➖➖➖➖➖➖➖➖➖➖
        
Теги: {", ".join(map(lambda x: x.tag, animal_filter.tags))}"""

    if edit:
        if add_keyboard:
            await message.edit_text(text, reply_markup=keyboards.animal_filter_keyboard())
        else:
            await message.edit_text(text, reply_markup=message.reply_markup)

    else:
        if add_keyboard:
            await message.answer(text, reply_markup=keyboards.animal_filter_keyboard())
        else:
            await message.answer(text, reply_markup=message.reply_markup)
