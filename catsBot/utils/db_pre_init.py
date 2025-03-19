from data import db_session
from data.animals_tags import AnimalTag
from config import ANIMAL_TAGS
from data.statistics import Statistic


def db_pre_init():
    session = db_session.create_session()
    for tag in ANIMAL_TAGS:
        old_tag = session.query(AnimalTag).where(AnimalTag.tag == tag).first()
        if old_tag is None:
            tag_model = AnimalTag(tag=tag)
            session.add(tag_model)

    statistic = session.query(Statistic).first()
    if statistic is None:
        session.add(Statistic())
        session.commit()
    session.commit()

