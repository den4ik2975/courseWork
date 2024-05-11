from sqlalchemy import Column, Integer, String, JSON

from src.database.base import Base


class Variant(Base):
    __tablename__ = 'variants'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    connections = Column(JSON)
    start = Column(String)
    end = Column(String)
    answers = Column(JSON)
