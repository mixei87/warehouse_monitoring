from uuid import UUID

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Stock(Base):
    """Модель остатков товаров на складе
    warehouse_id: ID склада (часть первичного ключа)
    product_id: ID товара (часть первичного ключа)
    quantity: Количество товара на складе
    """

    __tablename__ = "stocks"
    __repr_cols__ = ("warehouse_id", "product_id", "quantity")

    warehouse_id: Mapped[UUID] = mapped_column(
        ForeignKey("warehouses.id", ondelete="CASCADE"),
        primary_key=True,
        doc="ID склада",
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), primary_key=True, doc="ID товара"
    )

    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, doc="Количество товара на складе"
    )

    __table_args__ = (
        # Индекс для ускорения поиска по product_id
        {"postgresql_using": "btree"},
    )
