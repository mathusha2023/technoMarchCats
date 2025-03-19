import sqlalchemy
from .db_session import SqlAlchemyBase


class Question(SqlAlchemyBase):
    __tablename__ = "questions"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String)
    sender = sqlalchemy.Column(sqlalchemy.Integer)
    sender_name = sqlalchemy.Column(sqlalchemy.String)
    moderator = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("moderators.id"))
    message_ids = sqlalchemy.orm.relationship("MessageId")
