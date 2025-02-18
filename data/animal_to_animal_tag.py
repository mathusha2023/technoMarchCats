import sqlalchemy
from .db_session import SqlAlchemyBase

AnimalToAnimalTag = sqlalchemy.Table('animalToAnimalTag',
                                     SqlAlchemyBase.metadata,
                                     sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True),
                                     sqlalchemy.Column('animalId', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('animals.id')),
                                     sqlalchemy.Column('tagId', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('animalTags.id')))
