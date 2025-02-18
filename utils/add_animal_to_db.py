from sqlalchemy import desc
from data import db_session
from data.animals import Animal
from data.animals_images import AnimalImage


def add_animal_to_db(data):
    session = db_session.create_session()
    a = session.query(Animal).order_by(desc(Animal.id)).first()  # получаем id последнего животного для подвязки фотогафий
    if a is None:
        i = 1
    else:
        i = a.id + 1
    name = data["name"]
    gender = data["gender"]
    birthday = data["birthday"]
    description = data["description"]
    photos = data["photos"]
    for photo in photos:
        image = AnimalImage()  # добавляем обьекты фотографий с привязкой к животным
        image.animalId = i
        image.image = photo
        session.add(image)
    animal = Animal(name=name, birthDate=birthday, description=description, gender=gender)
    session.add(animal)
    session.commit()

