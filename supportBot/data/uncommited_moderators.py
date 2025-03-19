import sqlalchemy
from .db_session import SqlAlchemyBase


class UncommitedModerator(SqlAlchemyBase):
    __tablename__ = "uncommited_moderators"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
