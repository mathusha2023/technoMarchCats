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

    text = f"""Привет! Я {name}, {get_text_gender(gender)}, мне {delta.days // 365} лет и {delta.days % 365 // 30} месяцев.\n{description}\nТеги: {", ".join(map(lambda x: x.tag, tags))}"""

    album_builder = MediaGroupBuilder(
        caption=text
    )
    for photo in photos:
        album_builder.add_photo(photo)

    await message.answer_media_group(album_builder.build())
