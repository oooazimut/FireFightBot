from datetime import datetime
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


dttm = Annotated[datetime, mapped_column(default=datetime.now)]
classic_id = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"


class Pressure(Base):
    __tablename__ = "pressures"

    id: Mapped[classic_id]
    value: Mapped[float]
    dttm: Mapped[dttm]

    def __repr__(self) -> str:
        return f"Pressure(id={self.id!r}, value={self.value!r}, dttm={self.dttm!r})"


class WaterLevel(Base):
    __tablename__ = "water_levels"

    id: Mapped[classic_id]
    value: Mapped[float]
    dttm: Mapped[dttm]

    def __repr__(self) -> str:
        return f"WaterLevel(id={self.id!r}, value={self.value!r}, dttm={self.dttm!r})"


class PumpCondition(Base):
    __tablename__ = "pump_condition"

    id: Mapped[classic_id]
    condition: Mapped[int]
    dttm: Mapped[dttm]

    def __repr__(self) -> str:
        return f"PumpCondition(id={self.id!r}, condition={self.condition!r}, dttm={self.dttm!r})"
