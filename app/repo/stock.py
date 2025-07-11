from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.stock import Stock


class StockRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_stock(
        self,
        warehouse_id: UUID,
        product_id: UUID,
    ) -> Stock | None:
        """Получить информацию о количестве товара на складе."""
        result = await self.db.execute(
            select(Stock).where(
                and_(
                    Stock.warehouse_id == warehouse_id,
                    Stock.product_id == product_id,
                )
            )
        )
        return result.scalars().first()
