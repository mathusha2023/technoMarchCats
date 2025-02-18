import sqlalchemy
from sqlalchemy import orm
from datetime import date
from .db_session import SqlAlchemyBase
from .animal_to_animal_tag import AnimalToAnimalTag


class Animal(SqlAlchemyBase):
    __tablename__ = 'animals'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    birthDate = sqlalchemy.Column(sqlalchemy.Date)
    description = sqlalchemy.Column(sqlalchemy.String)
    images = orm.relationship("AnimalImage")
    tags = orm.relationship('AnimalTag', secondary=AnimalToAnimalTag, back_populates="animals")


    # возраст животного в годах
    def get_age(self):
        now = date.today()
        delta = now - self.birthDate
        return delta.days // 365
