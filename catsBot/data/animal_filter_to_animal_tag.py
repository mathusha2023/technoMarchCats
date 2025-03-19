import sqlalchemy
from .db_session import SqlAlchemyBase

# промежуточная таблица для связи между фильтрами животных и тегами
AnimalFilterToAnimalTag = sqlalchemy.Table('animalFilterToAnimalTag',
                                     SqlAlchemyBase.metadata,
                                     sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True),
                                     sqlalchemy.Column('animalFilterId', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('animalsFilters.id')),
                                     sqlalchemy.Column('tagId', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('animalTags.id')))
