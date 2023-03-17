from databases import Database
from loguru import logger
from tenacity import RetryError, retry, stop_after_delay, wait_exponential

from . import config

db = Database(config.DATABASE_URL, force_rollback=config.TESTING)


async def startup() -> None:
    show_config()
    await connect_database(db)
    logger.info('started...')


async def shutdown() -> None:
    await db.disconnect()
    logger.info('...shutdown')


def show_config() -> None:
    config_vars = {key: getattr(config, key) for key in sorted(dir(config)) if key.isupper()}
    logger.debug(config_vars)
    return


async def connect_database(database: Database) -> None:
    @retry(stop=stop_after_delay(3), wait=wait_exponential(multiplier=0.2))
    async def _connect_to_db() -> None:
        logger.info('Connecting to the database...')
        await database.connect()

    try:
        await _connect_to_db()
    except RetryError:
        logger.error('Could not connect to the database.')
        raise
