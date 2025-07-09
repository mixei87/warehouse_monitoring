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

    # Связи с движениями
    incoming_movements: Mapped[list["Movement"]] = relationship(
        "Movement",
        foreign_keys="[Movement.warehouse_id]",
        back_populates="warehouse",
        cascade="all, delete-orphan",
    )

    outgoing_movements: Mapped[list["Movement"]] = relationship(
        "Movement",
        foreign_keys="[Movement.source_id]",
        back_populates="source_warehouse",
        cascade="all, delete-orphan",
    )
