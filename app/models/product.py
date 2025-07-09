from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, uuid_pk, long_string

if TYPE_CHECKING:
    from app.models.stock import Stock


class Product(Base):
    """Модель товара
    id: Уникальный идентификатор UUID
    name: Название товара
    """

    __tablename__ = "products"
    __repr_cols__ = ("name",)

    id: Mapped[uuid_pk]
    name: Mapped[long_string] = mapped_column(doc="Название товара")

    # Связи
    stock_records: Mapped[list["Stock"]] = relationship(
        "WarehouseStock", back_populates="product", cascade="all, delete-orphan"
    )
