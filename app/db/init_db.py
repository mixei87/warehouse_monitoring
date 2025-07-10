from logging import getLogger

from sqlalchemy import text

from app.db.session import engine, sync_engine
from app.models import Base, Movement

logger = getLogger(__name__)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("All tables dropped")


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("All tables created")

    sql = Movement.get_sql_trigger_movement_after_insert()
    with sync_engine.connect() as conn:
        with conn.begin():
            conn.execute(text(sql))
    logger.info("Trigger registered")


async def init_db():
    """Инициализация базы данных (создание таблиц)"""
    # # Удаляем все таблицы (для разработки)
    # logger.info("Starting up...")
    # await drop_db()
    # # Создаем все таблицы
    # await create_tables()
    # logger.info("Database initialized")
    pass
