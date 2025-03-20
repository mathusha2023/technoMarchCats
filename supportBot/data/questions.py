import sqlalchemy
from .db_session import SqlAlchemyBase


# таблица вопросов
class Question(SqlAlchemyBase):
    __tablename__ = "questions"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String)
    sender = sqlalchemy.Column(sqlalchemy.Integer)
    sender_name = sqlalchemy.Column(sqlalchemy.String)
    moderator = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(
        "moderators.id"))  # модератор, который должен ответить на вопрос, выбирается при получении вопроса
    message_ids = sqlalchemy.orm.relationship("MessageId")
