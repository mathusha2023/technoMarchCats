from data import db_session
from data.animal_to_animal_tag import AnimalToAnimalTag
from data.animals import Animal
from data.animals_tags import AnimalTag
from sqlalchemy import select


def best_match(tags: list):
    session = db_session.create_session()
    
    # Получаем имена всех животных
    names = session.execute(select(Animal.name)).scalars().all()
    
    # Создаем словарь для хранения количества совпадений тегов
    names_dict = {name: 0 for name in names}
    
    # Для каждого животного находим его теги и считаем совпадения
    for name in names:
        id_ = session.execute(select(Animal.id).where(Animal.name == name)).scalar()
        animal_tags = session.query(AnimalTag).join(AnimalToAnimalTag).filter(AnimalToAnimalTag.c.animalId == id_).all()

        # Считаем количество совпадений тегов
        names_dict[name] = len(set(tags) & set(animal_tags))
    
    # Сортируем по количеству совпадений и возвращаем лучшее совпадение
    try:
        best_match = sorted(names_dict.items(), key=lambda x: x[1], reverse=True)[0][0]  # Берем первый элемент
        return best_match
    except IndexError:
        return "Не найдено"