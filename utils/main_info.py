from sqlalchemy.orm import Session
from .db_session import create_session

def get_animal_info(animal_name: str):
    session = create_session()
    animal = session.query(Animal).filter(Animal.name == animal_name).first()
    if animal is None:
        return None
    return {
        'name': animal.name,
        'gender': animal.gender,
        'birthday': animal.birthDate,
        'description': animal.description,
        'photos': [image.url for image in animal.images],
        'tags': [tag.name for tag in animal.tags]
    }
