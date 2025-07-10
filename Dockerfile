FROM python:3.12-slim as builder

WORKDIR /warehouse

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости в отдельную директорию
RUN pip install --user -r requirements.txt

# Финальный образ
FROM python:3.12-slim

WORKDIR /warehouse

# Копируем зависимости из builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Копируем остальные файлы
COPY app ./app
COPY .env .
COPY alembic.ini .

# Настройки окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/warehouse \
    ENVIRONMENT=development \
    DEBUG=true

# Команда для запуска
CMD uvicorn app.main:app --host "${APP_HOST}" --port "${APP_EXPOSED_PORT}" --reload
