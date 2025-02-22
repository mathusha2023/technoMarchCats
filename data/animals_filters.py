import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from .animal_filter_to_animal_tag import AnimalFilterToAnimalTag


class AnimalFilter(SqlAlchemyBase):
    __tablename__ = "animalsFilters"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    userId = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey("users.id"))
    minAge = sqlalchemy.Column(sqlalchemy.Integer, default=0)  # минимальный возраст питомца
    maxAge = sqlalchemy.Column(sqlalchemy.Integer, default=14)  # максимальный возраст питомца
    gender = sqlalchemy.Column(sqlalchemy.Integer, default=2)  # 0 - мальчик, 1 - девочка, 2 - оба пола
    tags = orm.relationship('AnimalTag', secondary=AnimalFilterToAnimalTag, back_populates="filters")

