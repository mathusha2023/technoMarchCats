import sqlalchemy
from sqlalchemy import orm
from datetime import date
from .db_session import SqlAlchemyBase
from .animal_to_animal_tag import AnimalToAnimalTag


# животные
class Animal(SqlAlchemyBase):
    __tablename__ = 'animals'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    gender = sqlalchemy.Column(sqlalchemy.Integer)  # 0 - мальчик, 1 - девочка
    birthDate = sqlalchemy.Column(sqlalchemy.Date)
    description = sqlalchemy.Column(sqlalchemy.String)
    images = orm.relationship("AnimalImage", backref="animals", passive_deletes=True)
    tags = orm.relationship('AnimalTag', secondary=AnimalToAnimalTag, back_populates="animals")

    # возраст животного в годах
    def get_age(self):
        now = date.today()
        delta = now - self.birthDate
        return delta.days // 365, delta.days % 365 // 30