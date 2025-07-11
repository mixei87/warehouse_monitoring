from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, uuid_pk, long_string


class Product(Base):
    """Модель товара
    id: Уникальный идентификатор UUID
    name: Название товара
    """

    __tablename__ = "products"
    __repr_cols__ = ("name",)

    id: Mapped[uuid_pk]
    name: Mapped[long_string] = mapped_column(doc="Название товара")
