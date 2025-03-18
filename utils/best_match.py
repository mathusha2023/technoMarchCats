from data import db_session
from data.animals_tags import AnimalTag
from config import ANIMAL_TAGS


def best_match(tags: list):
    session = db_session.create_session()
    names = session.select(Animal.name).all()
    names_dict = dict.fromkeys(names, 0)
    for name in names:
        tags_in_db = session.query(AnimalTag).join(AnimalToAnimalTag).join(Animal).filter(Animal.name == name).all()
        names_dict[name] = len(set(tags) & set(tags_in_db))
    best_match = max(names_dict, key=names_dict.get)
    return best_match

