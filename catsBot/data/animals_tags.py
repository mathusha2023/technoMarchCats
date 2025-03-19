import sqlalchemy
from sqlalchemy import orm
from .animal_filter_to_animal_tag import AnimalFilterToAnimalTag
from .db_session import SqlAlchemyBase
from .animal_to_animal_tag import AnimalToAnimalTag


class AnimalTag(SqlAlchemyBase):
    __tablename__ = "animalTags"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    tag = sqlalchemy.Column(sqlalchemy.String, nullable=False, index=True)
    animals = orm.relationship('Animal', secondary=AnimalToAnimalTag, back_populates="tags")
    filters = orm.relationship('AnimalFilter', secondary=AnimalFilterToAnimalTag, back_populates="tags")
