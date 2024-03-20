from random import randint

from sqlalchemy.orm import Session
from database.tables import Variant
from database.base import session


def get_random_variant() -> Variant:
    chosen_variant = randint(0, 19)

    return session.query(Variant).filter(Variant.id == chosen_variant).one_or_none

