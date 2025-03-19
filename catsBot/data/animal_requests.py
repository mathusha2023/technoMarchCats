from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

# заявки на опекунство
class AnimalRequest(SqlAlchemyBase):
    __tablename__ = 'animal_requests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    createdAt = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now())
    userId = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey("users.id"))
    animalId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("animals.id"))
    user = orm.relationship("User", uselist=False, backref="animal_requests")
    animal = orm.relationship("Animal", uselist=False, backref="animal_requests")
