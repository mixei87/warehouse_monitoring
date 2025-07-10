import os.path
from pathlib import Path
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Integer,
    Enum as SQLEnum,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, timestamp_type, MovementType


class Movement(Base):
    """Модель движения товаров
    Атрибуты:
        id: Уникальный идентификатор UUID
        movement_id: ID перемещения для группировки связанных событий
        warehouse_id: ID склада, на котором изменяются остатки
        product_id: ID товара
        event_type: Тип события (arrival/departure)
        quantity: Количество товара (должно быть положительным)
        timestamp: Временная метка события
    """

    __tablename__ = "movements"
    __repr_cols__ = ("warehouse_id", "product_id", "event_type", "quantity")
    __table_args__ = (CheckConstraint("quantity > 0", name="check_quantity_positive"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    movement_id: Mapped[UUID] = mapped_column(
        index=True,
        nullable=False,
        doc="ID перемещения для группировки связанных событий",
    )
    warehouse_id: Mapped[UUID] = mapped_column(
        ForeignKey("warehouses.id", ondelete="CASCADE"),
        nullable=False,
        doc="ID склада, на котором изменяются остатки",
    )
    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        doc="ID товара",
    )
    event_type: Mapped[MovementType] = mapped_column(
        SQLEnum(MovementType, name="movement_type"),
        nullable=False,
        doc="Тип движения (приход/уход)",
    )
    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, doc="Количество товара (не может быть отрицательным)"
    )
    timestamp: Mapped[timestamp_type]

    warehouse = relationship("Warehouse", back_populates="movements")

    @classmethod
    def get_sql_trigger_movement_after_insert(cls) -> str:
        try:
            trigger_path = os.path.join(
                Path(__file__).parent, "sql/triggers/update_warehouse_stock_trigger.sql"
            )
            with open(trigger_path) as f:
                sql = f.read()
            return sql
        except FileNotFoundError as e:
            raise FileNotFoundError(e)
        except Exception as e:
            raise Exception(e)
