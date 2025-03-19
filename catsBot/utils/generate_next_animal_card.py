from aiogram.types import Message
from datetime import date, timedelta
from sqlalchemy import and_
from functools import reduce
from data.animals_filters import AnimalFilter
from data.db_session import create_session
from data.users import User
from data.animals import Animal
from aiogram.utils.media_group import MediaGroupBuilder
from utils.get_text_gender import get_text_gender

# генерация карточки следующего животного в списке животных
async def generate_next_animal_card(user_id, message: Message):
    session = create_session()
    user = session.query(User).where(User.id == user_id).first()
    animal_filter: AnimalFilter = user.filter
    min_date = date.today() - timedelta(days=animal_filter.maxAge * 365)
    max_date = date.today() - timedelta(days=animal_filter.minAge * 365)

    s = []
    for tag in animal_filter.tags:
        a = set()
        for tags_animal in tag.animals:
            a.add(tags_animal.id)
        s.append(a)

    if animal_filter.tags:  # если теги есть
        s = [i for i in reduce(lambda x, y: x.intersection(y), s)]  # получаем айди животных, которые подойдут пользователю по фильтрам
        if animal_filter.gender > 1:  # фильтр для любого пола
            condition = and_(Animal.id > user.lastWatchedAnimal, Animal.birthDate.between(min_date, max_date),
                             Animal.id.in_(s))

        else:  # фильтр для конкретного пола
            condition = and_(Animal.id > user.lastWatchedAnimal, Animal.birthDate.between(min_date, max_date),
                             Animal.gender == animal_filter.gender, Animal.id.in_(s))
    else:
        if animal_filter.gender > 1:  # фильтр для любого пола
            condition = and_(Animal.id > user.lastWatchedAnimal, Animal.birthDate.between(min_date, max_date))

        else:  # фильтр для конкретного пола
            condition = and_(Animal.id > user.lastWatchedAnimal, Animal.birthDate.between(min_date, max_date),
                             Animal.gender == animal_filter.gender)

    animal = session.query(Animal).where(condition).first()

    if animal is None:  # может быть животное было последним в списке, надо попробовать поискать с самого начала

        if animal_filter.tags:  # если теги есть
            if animal_filter.gender > 1:  # фильтр для любого пола
                condition = and_(Animal.birthDate.between(min_date, max_date), Animal.id.in_(s))

            else:  # фильтр для конкретного пола
                condition = and_(Animal.birthDate.between(min_date, max_date), Animal.gender == animal_filter.gender,
                                 Animal.id.in_(s))
        else:
            if animal_filter.gender > 1:  # фильтр для любого пола
                condition = Animal.birthDate.between(min_date, max_date)

            else:  # фильтр для конкретного пола
                condition = and_(Animal.birthDate.between(min_date, max_date), Animal.gender == animal_filter.gender)

        animal = session.query(Animal).where(condition).first()

    if animal is None:  # животное все равно не найдено, значит, под такой фильтр животного не существует
        user.lastWatchedAnimal = 0  # удаляем последнее просмотренное пользователем животное (надо для работы системы заявок)
        session.commit()
        return await message.answer("Котиков под ваши фильтры не найдено:( Попробуйте изменить набор значений в фильтре")
    user.lastWatchedAnimal = animal.id
    session.commit()

    y, m = animal.get_age()
    text = f"""Привет! Я {animal.name}, {get_text_gender(animal.gender)}, мне {y} лет и {m} месяцев.\n{animal.description}\nТеги: {", ".join(map(lambda x: x.tag, animal.tags))}"""

    album_builder = MediaGroupBuilder(
        caption=text
    )
    for photo in animal.images:
        album_builder.add_photo(photo.image)

    await message.answer_media_group(album_builder.build())
