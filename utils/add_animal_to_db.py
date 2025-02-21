from sqlalchemy import desc
from data.animals import Animal
from data.animals_images import AnimalImage


async def add_animal_to_db(data):
    session = data["db_session"]
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
    tags = data["tags"]
    for photo in photos:
        image = AnimalImage()  # добавляем обьекты фотографий с привязкой к животным
        image.animalId = i
        image.image = photo
        session.add(image)
    animal = Animal(id=i, name=name, birthDate=birthday, description=description, gender=gender, tags=tags)
    session.add(animal)
    session.commit()
