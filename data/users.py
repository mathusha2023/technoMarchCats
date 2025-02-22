import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.String)
    first_name = sqlalchemy.Column(sqlalchemy.String)
    accessLevel = sqlalchemy.Column(sqlalchemy.Integer, default=1, nullable=False)  # права пользователя: 1 - простой пользователь, 2 - администратор, 3 - супер-админ
    lastWatchedAnimal = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    filter = orm.relationship("AnimalFilter", uselist=False, backref="user")
