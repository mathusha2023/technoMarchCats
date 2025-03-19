import sqlalchemy
from .db_session import SqlAlchemyBase


class MessageId(SqlAlchemyBase):
    __tablename__ = "message_ids"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    message_id = sqlalchemy.Column(sqlalchemy.Integer)
    question = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("questions.id"))
