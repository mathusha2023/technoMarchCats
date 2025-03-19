from data.animals import Animal
from data.animals_images import AnimalImage


# обновление информации животного из словаря
async def update_animal_information(data):
    session = data["session"]
    animal_id = data["id"]
    name = data["name"]
    gender = data["gender"]
    birthday = data["birthday"]
    description = data["description"]
    photos = data["photos"]
    tags = data["tags"]

    animal = session.query(Animal).where(Animal.id == animal_id).first()
    animal.name = name
    animal.gender = gender
    animal.birthDate = birthday
    animal.description = description
    for image in animal.images:
        session.delete(image)
    # animal.images.clear()
    animal.tags = tags

    for photo in photos:
        image = AnimalImage()  # добавляем обьекты фотографий с привязкой к животным
        image.animalId = animal_id
        image.image = photo
        session.add(image)

    session.commit()
