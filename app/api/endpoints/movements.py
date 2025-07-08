from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.movement import MovementResponse
from app.services.movement import MovementService

router = APIRouter()


@router.get("/{movement_id}", response_model=list[MovementResponse])
async def read_movement(movement_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Получить информацию о перемещении по ID.

    Возвращает информацию о перемещении по его ID, включая отправителя, получателя, время, прошедшее между отправкой и
    приемкой, и разницу в количестве товара
    """
    service = MovementService(db)
    movements = await service.get_movement_info(movement_id)
    if not movements:
        raise HTTPException(status_code=404, detail="Перемещение не найдено")
    return movements
