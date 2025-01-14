import asyncio
import os
from pathlib import Path
from subprocess import run

from poll import config
from poll.resources import Database, connect_database

parent_path = Path(__file__).parent


async def migrate() -> None:
    """
    Wait for the database to be ready.
    """
    db = Database(config.DATABASE_URL)
    await connect_database(db)
    await db.disconnect()
    run('alembic upgrade head'.split(), cwd=parent_path)
    return


async def main() -> None:
    command = 'hypercorn --config=hypercorn.toml poll.main:app'.split()
    if os.getenv('ENV') != 'production':
        await migrate()
        command.insert(1, '--reload')
    run(command, cwd=parent_path)
    return


if __name__ == '__main__':
    asyncio.run(main())
