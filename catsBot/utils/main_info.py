from sqlalchemy.orm import Session, joinedload
from data.db_session import create_session
from sqlalchemy import select, func
from data.animals import Animal
from data.animals_images import AnimalImage

def get_animal_info(animal_name: str):
    session = create_session()
    query = (
        select(
            Animal.name,
            Animal.gender,
            Animal.birthDate,
            Animal.description,
            AnimalImage,
            func.group_concat(AnimalTag.name) # Агрегируем теги в строку
        )
        .join(AnimalImage, Animal.images, isouter=True)  # Присоединяем таблицу AnimalImage (LEFT JOIN)
        .join(AnimalToAnimalTag, Animal.tags, isouter=True)  # Присоединяем таблицу AnimalToAnimalTag (LEFT JOIN)
        .join(AnimalTag, AnimalToAnimalTag.c.animal_tag_id == AnimalTag.id, isouter=True)  # Присоединяем таблицу AnimalTag (LEFT JOIN)
        .where(Animal.name == animal_name)
        .group_by(Animal.id)  # Группируем по животному, чтобы агрегировать теги
        .limit(1)  # Ограничиваем результат одним животным
    )
    data = session.execute(query).fetchone()._asdict()
    if data is None:
        return None
    data["birthday"] = data["birthDate"]
    data["photos"] = [data["AnimalImage"]]
    return data

