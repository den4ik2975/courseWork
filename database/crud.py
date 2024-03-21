from random import randint

from sqlalchemy import select
from database.tables import Variant
from database.base import session


def get_random_variant() -> Variant:
    #chosenVariant = randint(0, 19)
    chosen_variant = 1  # DEV

    stmt = select(Variant).where(Variant.id == chosen_variant)

    # Execute the query and fetch one result.
    with session:
        variant = session.execute(stmt).scalars().first()
        return variant


def add_new_variant(data: dict, ans: dict) -> None:  # DEV!!!
    with session:
        var = Variant(
            connections=data['data'],
            start=data['start'],
            end=data['end'],
            answers=ans
        )

        session.add(var)
        session.commit()

