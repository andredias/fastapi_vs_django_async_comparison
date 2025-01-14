from pathlib import Path
from secrets import randbelow

from sqlalchemy import MetaData

metadata = MetaData()

# metadata.tables is only populated after all models are imported.
# see alembic/env.py for an example.
modules = Path(__file__).parent.glob('*.py')
__all__ = [p.stem for p in modules if p.is_file() and p.stem != '__init__']

MAX_ID = 2**31


def random_id() -> int:
    """
    Return a random integer to be used as ID.

    Auto-incremented IDs are not particularly good for users as primary keys.
    1. Sequential IDs are guessable.
       One might guess that admin is always user with ID 1, for example.
    2. Tests end up using fixed ID values such as 1 or 2 instead of real values.
       This leads to poor test designs that should be avoided.
    """
    return randbelow(MAX_ID)
