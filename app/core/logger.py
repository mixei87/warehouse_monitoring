import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging():
    # Создаем директорию для логов, если её нет
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Формат логов
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # Обработчик для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    # Устанавливаем уровень логирования из переменной окружения или DEBUG по умолчанию
    console_handler.setLevel(logging.DEBUG)

    # Обработчик для файла с ошибками
    error_file_handler = RotatingFileHandler(
        "logs/error.log", maxBytes=10485760, backupCount=5
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)

    # Обработчик для общего лога
    info_file_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=10485760, backupCount=5
    )
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(formatter)

    # Корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(error_file_handler)
    root_logger.addHandler(info_file_handler)

    # Настройка логгера SQLAlchemy
    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_logger.setLevel(logging.WARNING)
