from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_product_by_id(
        self,
        product_id: UUID,
    ) -> Product | None:
        """Получить информацию о продукте"""
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        return result.scalars().first()
