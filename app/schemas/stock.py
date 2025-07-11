from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class StockResponse(BaseModel):
    warehouse_id: UUID
    product_id: UUID
    quantity: int = Field(
        ge=0, description="Количество товара (не может быть отрицательным)"
    )

    model_config = ConfigDict(from_attributes=True)
