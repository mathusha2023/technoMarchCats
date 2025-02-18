import sqlalchemy
from .db_session import SqlAlchemyBase


class AnimalImage(SqlAlchemyBase):
    __tablename__ = "animalImages"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    animalId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("animals.id"))
    image = sqlalchemy.Column(sqlalchemy.String)  # храним не бинарники изображений, а их telegram id
