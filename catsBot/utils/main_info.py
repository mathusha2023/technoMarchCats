from sqlalchemy.orm import Session, joinedload
from data.db_session import create_session
from sqlalchemy import select, func
from data.animals import Animal
from data.animals_images import AnimalImage

def get_animal_info(animal_name: str):
    session = create_session()
    animal = session.query(Animal).where(Animal.name == animal_name).first()
    data = {}  # сюда заносим данные животного в виде словаря
    if animal is None:
        return
    data["birthday"] = data["birthDate"]
    data["photos"] = [data["AnimalImage"]]
    return data

