from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Pressure(Base):
    __tablename__ = "pressures"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    value: Mapped[float]
    dttm: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class WaterLevel(Base):
    __tablename__ = "water_levels"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    value: Mapped[float]
    dttm: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
