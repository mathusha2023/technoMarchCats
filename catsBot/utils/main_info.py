from sqlalchemy.orm import Session, joinedload
from data.db_session import create_session
from sqlalchemy import select, func
from data.animals import Animal
from data.animals_images import AnimalImage


# получаем словарь информации о животном по id
def get_animal_info(id_: str):
    session = create_session()
    animal = session.query(Animal).where(Animal.id == id_).first()

    if animal is None:
        return None  # Если животное не найдено, возвращаем None

    # Преобразуем объект Animal в словарь
    data = animal.__dict__

    # Убираем ненужные ключи (например, "_sa_instance_state")
    data = {key: value for key, value in data.items() if not key.startswith("_")}

    # Добавляем поле "birthday" (если нужно)
    data["birthday"] = data.pop("birthDate", None)

    # Добавляем фото (строковые значения URL)
    data["photos"] = [image.image for image in animal.images] if animal.images else []

    # Добавляем теги (строковые значения)
    data["tags"] = animal.tags

    return data
