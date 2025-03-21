import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


# объект пользователя
class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True, nullable=False)  # telegram user_id
    username = sqlalchemy.Column(sqlalchemy.String)  # telegram username
    firstName = sqlalchemy.Column(sqlalchemy.String)  # имя из telegram
    accessLevel = sqlalchemy.Column(sqlalchemy.Integer, default=1, nullable=False)  # права пользователя: 1 - простой пользователь, 2 - администратор, 3 - супер-админ
    lastWatchedAnimal = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    isBanned = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=False)
    isVolunteer = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=False)
    filter = orm.relationship("AnimalFilter", uselist=False, backref="user")
