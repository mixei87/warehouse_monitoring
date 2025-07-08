from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.warehouse import WarehouseStockResponse
from app.services.warehouse import WarehouseService

router = APIRouter()


@router.get(
    "/{warehouse_id}/products/{product_id}", response_model=WarehouseStockResponse
)
async def read_warehouse_stock(
    warehouse_id: UUID,
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Получить текущие остатки товаров на складе.

    Возвращает информацию о текущем запасе товара в конкретном складе
    """
    service = WarehouseService(db)
    try:
        return await service.get_product_stock_by_id(
            warehouse_id=warehouse_id, product_id=product_id
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
