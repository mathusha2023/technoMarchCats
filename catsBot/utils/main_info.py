from sqlalchemy.orm import Session, joinedload
from data.db_session import create_session
from sqlalchemy import select, func
from data.animals import Animal
from data.animals_images import AnimalImage

def get_animal_info(animal_name: str):
    session = create_session()
    query = (
        session.query(Animal)
        .options(
            joinedload(Animal.images),  # Загружаем связанные фото
            joinedload(Animal.tags)     # Загружаем связанные теги
        )
        .filter(Animal.name == animal_name)
        .first()  # Получаем первое совпадение
    )
    data = session.execute(query).fetchone()._asdict()
    if data is None:
        return None
    data["birthday"] = data["birthDate"]
    data["photos"] = data["AnimalImage"]
    return data
    