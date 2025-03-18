import sqlalchemy
from sqlalchemy import orm
from datetime import date
from .db_session import SqlAlchemyBase
from .animal_to_animal_tag import AnimalToAnimalTag


class Statistic(SqlAlchemyBase):
    __tablename__ = 'statistic'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    donatesCount = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=False)
    donatesSum = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=False)  # RUB
