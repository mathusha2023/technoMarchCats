from sqlalchemy.orm import Session
from data.db_session import create_session
from sqlalchemy import select
from data.animals import Animal

def get_animal_info(animal_name: str):
    session = create_session()
    query = select(Animal.name, Animal.gender, Animal.birthDate, Animal.description).where(Animal.name == animal_name)
    data = session.execute(query).fetchall()
    print(data)
    return data
