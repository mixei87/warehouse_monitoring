from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.core.deps import StockServiceDepends
from app.core.utils import AppError
from app.schemas.stock import StockResponse

router = APIRouter(prefix="/warehouses", tags=["warehouses"])


@router.get(
    "/{warehouse_id}/products/{product_id}",
    response_model=StockResponse,
    summary="Получить количество товара на складе",
    description="Возвращает информацию о количестве указанного товара на указанном складе",
)
async def get_product_stock(
    warehouse_id: UUID,
    product_id: UUID,
    stock_service: StockServiceDepends,
) -> StockResponse:
    try:
        stock = await stock_service.get_stock(warehouse_id, product_id)
        if stock is None:
            raise HTTPException(
                status_code=404,
                detail=f"Остаток для товара {product_id} на складе {warehouse_id} не найден",
            )
        return StockResponse.model_validate(stock)
    except AppError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
