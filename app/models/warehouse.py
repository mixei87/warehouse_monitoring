from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, short_string, uuid_pk

if TYPE_CHECKING:
    from app.models.movement import Movement


class Warehouse(Base):
    """Модель склада
    id: Уникальный идентификатор UUID
    source: Идентификатор склада в формате WH-XXXX
    """

    __tablename__ = "warehouses"
    __repr_cols__ = ("source",)

    id: Mapped[uuid_pk]
    source: Mapped[short_string] = mapped_column(
        doc="Идентификатор склада в формате WH-XXXX"
    )

    # Все перемещения, связанные со складом (как входящие, так и исходящие)
    movements: Mapped[list["Movement"]] = relationship(
        "Movement",
        foreign_keys="[Movement.warehouse_id]",
        back_populates="warehouse",
        cascade="all, delete-orphan",
    )
