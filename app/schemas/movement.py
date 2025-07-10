from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class MovementType(str, Enum):
    ARRIVAL = "arrival"
    DEPARTURE = "departure"


class MovementCreate(BaseModel):
    """Схема для создания записи о перемещении товара.
    Атрибуты:
        id: Уникальный идентификатор записи (UUID)
        movement_id: Идентификатор перемещения для группировки событий (UUID)
        warehouse_id: Идентификатор склада, на котором изменяются остатки (UUID)
        product_id: Идентификатор товара (UUID)
        quantity: Количество товара (целое положительное число)
        event_type: Тип события (arrival/departure)
        timestamp: Временная метка события
    """

    id: UUID
    movement_id: UUID
    warehouse_id: UUID
    product_id: UUID
    quantity: int = Field(
        gt=0,
        le=2_147_483_647,
        description="Количество должно быть положительным числом",
    )
    event_type: MovementType
    timestamp: datetime


class MovementResponse(BaseModel):
    """Схема для ответа с информацией о перемещении.
    Атрибуты:
        id: Уникальный идентификатор записи (строка)
        movement_id: Идентификатор перемещения (строка)
        warehouse_id: Идентификатор склада (строка)
        product_id: Идентификатор товара (строка)
        quantity_diff: Разница в количестве товара
        elapsed_time: Время обработки в секундах (опционально)
    """

    id: UUID
    movement_id: UUID
    warehouse_id: UUID
    product_id: UUID
    quantity_diff: int
    elapsed_time: int | None = None

    model_config = ConfigDict(from_attributes=True)
