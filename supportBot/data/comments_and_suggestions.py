import sqlalchemy
from .db_session import SqlAlchemyBase


# таблица отзывов и пожеланий
class Suggestion(SqlAlchemyBase):
    __tablename__ = "suggestions"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String)
    sender = sqlalchemy.Column(sqlalchemy.Integer)
    sender_name = sqlalchemy.Column(sqlalchemy.String)
