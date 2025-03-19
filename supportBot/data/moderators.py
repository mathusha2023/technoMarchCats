import sqlalchemy
from .db_session import SqlAlchemyBase


class Moderator(SqlAlchemyBase):
    __tablename__ = "moderators"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.String, default="Moder")
    questions = sqlalchemy.orm.relationship("Question")
