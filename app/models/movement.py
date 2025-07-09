from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Integer,
    Enum as SQLEnum,
    CheckConstraint,
    event,
    DDL,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, timestamp_type, MovementType


class Movement(Base):
    """Модель движения товаров
    id: Уникальный идентификатор UUID
    warehouse_id: ID склада
    product_id: ID товара
    event_type: Тип события (приход/уход)
    quantity: Количество товара
    timestamp: Временная метка события
    """

    __tablename__ = "movements"
    __repr_cols__ = ("warehouse_id", "product_id", "event_type", "quantity")
    __table_args__ = (CheckConstraint("quantity >= 0", name="check_quantity_positive"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    movement_id: Mapped[UUID] = mapped_column(
        index=True, 
        nullable=False, 
        doc="ID перемещения для группировки связанных событий"
    )
    warehouse_id: Mapped[UUID] = mapped_column(
        ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False, doc="ID склада-получателя"
    )
    source_id: Mapped[UUID] = mapped_column(
        ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False, doc="ID склада-отправителя"
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

    warehouse = relationship("Warehouse", foreign_keys=[warehouse_id], back_populates="incoming_movements")
    source_warehouse = relationship("Warehouse", foreign_keys=[source_id], back_populates="outgoing_movements")

    @classmethod
    def register_trigger_update_quantity(cls):
        try:
            with open("sql/triggers/update_warehouse_stock_trigger.sql") as f:
                sql = f.read()
            update_quantity_trigger = DDL(sql)
            event.listen(cls, "after_insert", update_quantity_trigger)
        except FileNotFoundError as e:
            raise FileNotFoundError(e)
        except Exception as e:
            raise Exception(e)
