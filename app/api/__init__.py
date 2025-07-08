from fastapi import APIRouter
from app.api.endpoints import warehouses, movements

# Создаем основной роутер API
api_router = APIRouter(prefix="/api")

# Подключаем эндпоинты
api_router.include_router(warehouses.router, prefix="/warehouses", tags=["warehouses"])
api_router.include_router(movements.router, prefix="/movements", tags=["movements"])
