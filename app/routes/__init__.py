from fastapi import APIRouter

from app.routes.movement import router as movement_router
from app.routes.stock import router as stock_router

router = APIRouter(prefix="/api")

router.include_router(movement_router)
router.include_router(stock_router)
