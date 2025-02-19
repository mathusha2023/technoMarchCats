from aiogram.types import Message
from data.db_session import create_session
from data.users import User
from data.animals import Animal
from aiogram.utils.media_group import MediaGroupBuilder

from utils.get_text_gender import get_text_gender


async def generate_next_animal_card(user_id, message: Message):
    session = create_session()
    user = session.query(User).where(User.id == user_id).first()
    animal = session.query(Animal).where(Animal.id == user.lastWatchedAnimal + 1).first()
    if animal is None:
        animal = session.query(Animal).where(Animal.id == 1).first()
    if animal is None:
        return
    user.lastWatchedAnimal = animal.id
    session.commit()


    text = f"""Привет! Я {animal.name}, {get_text_gender(animal.gender)}, мне {animal.get_age()} лет.\n{animal.description}\nТеги: {", ".join(map(lambda x: x.tag, animal.tags))}"""

    album_builder = MediaGroupBuilder(
        caption=text
    )
    for photo in animal.images:
        album_builder.add_photo(photo.image)

    await message.answer_media_group(album_builder.build())
