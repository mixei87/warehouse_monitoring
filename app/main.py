from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI

from app.routes import router
from app.core.config import settings
from app.core.logger import setup_logging
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    # Настройка логирования
    setup_logging()
    logger = getLogger(__name__)
    # Старт приложения
    await init_db()
    yield
    # Остановка приложения
    logger.info("Shutting down...")


app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION, lifespan=lifespan)
app.include_router(router)
