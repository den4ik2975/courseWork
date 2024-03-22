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


def add_new_variant(connections, start, end, answers) -> None:  # DEV!!!
    with session:
        var = Variant(
            connections=connections,
            start=start,
            end=end,
            answers=answers
        )

        session.add(var)
        session.commit()

