from enum import Enum as PyEnum
from typing import Annotated
from uuid import UUID

from sqlalchemy import String, DateTime, text
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    repr_cols_num: int = 2
    repr_cols: tuple[...] = tuple()

    def __repr__(self):
        cols = [
            f"{col}={getattr(self, col)}"
            for idx, col in enumerate(self.__table__.columns.keys())
            if col in self.repr_cols or idx < self.repr_cols_num
        ]
        return f"<{self.__class__.__name__} {', '.join(cols)}>"


pk = Annotated[int, mapped_column(primary_key=True)]
uuid_pk = Annotated[
    UUID, mapped_column(primary_key=True, server_default=text("gen_random_uuid()"))
]
short_string = Annotated[str, mapped_column(String(20), unique=True, nullable=False)]
long_string = Annotated[str, mapped_column(String(255), unique=True, nullable=False)]
timestamp_type = Annotated[
    DateTime, mapped_column(DateTime(), server_default=text("TIMEZONE('utc', now())"))
]


class MovementType(PyEnum):
    ARRIVAL = "ARRIVAL"
    DEPARTURE = "DEPARTURE"
