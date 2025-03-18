from datetime import date
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder

from utils.get_text_gender import get_text_gender


async def generate_animal_card_by_state(data, message: Message):
    name = data["name"]
    gender = data["gender"]
    birthday: date = data["birthday"]
    description = data["description"]
    photos = data["photos"]
    tags = data["tags"]

    now = date.today()
    delta = now - birthday

    age = delta.days // 365
    month = delta // 30 - age * 12

    age_state = 'лет'
    month_state = 'месяцев' if month not in (0, 1) else 'месяц'
    if age < 1:
        age, age_state = month, month_state
    elif age == 1:
        age_state = 'год'
    elif 1 < age < 5:
        age_state = 'года'
    elif age >= 5:
        age_state = 'лет'

    if month:
        text = f"""Привет! Я {name}, {get_text_gender(gender)}, мне {age} {age_state} {month} {month_state}.\n{description}\nТеги: {", ".join(map(lambda x: x.tag, tags))}"""
    else:
        text = f"""Привет! Я {name}, {get_text_gender(gender)}, мне {age} {age_state}.\n{description}\nТеги: {", ".join(map(lambda x: x.tag, tags))}"""

    album_builder = MediaGroupBuilder(
        caption=text
    )
    for photo in photos:
        album_builder.add_photo(photo)

    await message.answer_media_group(album_builder.build())
