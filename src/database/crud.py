from random import randint

from sqlalchemy import select

from src.database.base import session
from src.database.tables import Variant


def get_random_variant() -> Variant:
    chosen_variant = randint(0, 19)

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
