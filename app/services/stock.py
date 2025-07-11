from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import AppError
from app.models import Stock
from app.repo.product import ProductRepository
from app.repo.stock import StockRepository
from app.repo.warehouse import WarehouseRepository


@dataclass(repr=False, eq=False, frozen=True, slots=True)
class StockService:
    """Сервис для работы с остатками товаров на складах"""

    db: AsyncSession
    stock_repo: StockRepository
    warehouse_repo: WarehouseRepository
    product_repo: ProductRepository

    async def get_stock(self, warehouse_id: UUID, product_id: UUID) -> Stock | None:
        """
        Получить информацию о количестве товара на складе.
        Args:
            warehouse_id: ID склада
            product_id: ID товара
        Returns:
            Информация об остатке товара или None, если запись не найдена
        Raises:
            AppError: Если склад или товар не найдены
        """
        if not await self.warehouse_repo.get_warehouse_by_id(warehouse_id):
            raise AppError(
                status_code=404, message=f"Склад с id={warehouse_id} не найден"
            )

        if not await self.product_repo.get_product_by_id(product_id):
            raise AppError(
                status_code=404, message=f"Товар с id={product_id} не найден"
            )

        return await self.stock_repo.get_stock(warehouse_id, product_id)
