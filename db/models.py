from datetime import datetime
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


dttm = Annotated[datetime, mapped_column(default=datetime.now().replace(microsecond=0))]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"


class Pressure(Base):
    __tablename__ = "pressures"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    value: Mapped[float]
    dttm: Mapped[dttm]

    def __repr__(self) -> str:
        return f"Pressure(id={self.id!r}, value={self.value!r}, dttm={self.dttm!r})"


class WaterLevel(Base):
    __tablename__ = "water_levels"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    value: Mapped[float]
    dttm: Mapped[dttm]

    def __repr__(self) -> str:
        return f"WaterLevel(id={self.id!r}, value={self.value!r}, dttm={self.dttm!r})"
