from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass

from src.database.tables import *

engine = create_engine('sqlite:///src/resources/data.db', echo=False)
Base.metadata.create_all(engine)
session = Session(engine)
