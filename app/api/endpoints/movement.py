from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_movement_service
from app.schemas.movement import MovementResponse
from app.services.movement import MovementService

router = APIRouter(prefix="/movements", tags=["movements"])


@router.get("/{movement_id}", response_model=list[MovementResponse])
async def read_movement(
    movement_id: UUID,
    movement_service: MovementService = Depends(get_movement_service)
):
    """
    Получить информацию о перемещении по ID.
    Возвращает информацию о перемещении по его ID, включая отправителя, получателя, время, прошедшее между отправкой и
    приемкой, и разницу в количестве товара
    Args:
        movement_id: Идентификатор перемещения
        movement_service: Сервис для работы с перемещениями
    Returns:
        Список событий перемещения
    Raises:
        HTTPException: 404 если перемещение не найдено
    """
    movements = await movement_service.get_movement_info(movement_id)
    if not movements:
        raise HTTPException(status_code=404, detail="Перемещение не найдено")
    return movements
