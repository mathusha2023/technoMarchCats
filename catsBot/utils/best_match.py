from data import db_session
from data.animal_to_animal_tag import AnimalToAnimalTag
from data.animals import Animal
from data.animals_tags import AnimalTag
from sqlalchemy import select


def best_match(tags: list):  # поиск наилучшего совпадения по тегам
    session = db_session.create_session()
    
    # Получаем id всех животных
    ids = session.execute(select(Animal.id)).scalars().all()
    
    # Создаем словарь для хранения количества совпадений тегов
    ids_dict = {id_: 0 for id_ in ids}
    
    # Для каждого животного находим его теги и считаем совпадения
    for id_ in ids:
        animal_tags = session.query(AnimalTag).join(AnimalToAnimalTag).filter(AnimalToAnimalTag.c.animalId == id_).all()

        # Считаем количество совпадений тегов
        ids_dict[id_] = len(set(tags) & set(animal_tags))
    
    # Сортируем по количеству совпадений и возвращаем лучшее совпадение
    try:
        best_match = sorted(ids_dict.items(), key=lambda x: x[1], reverse=True)[0][0]  # Берем первый элемент
        return best_match
    except IndexError:
        return "Не найдено"
