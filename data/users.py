import sqlalchemy

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.String)
    accessLevel = sqlalchemy.Column(sqlalchemy.Integer, default=1, nullable=False)  # права пользователя: 1 - простой пользователь, 2 - администратор, 3 - супер-админ
