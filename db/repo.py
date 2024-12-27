from datetime import date
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_last(session: AsyncSession, tables: list):
    result = []
    for table in tables:
        query = select(table).order_by(table.id.desc()).limit(1)
        data = await session.scalar(query)
        result.append(data)
    return result


async def get_by_date(session: AsyncSession, selected_date: date, models: list):
    result = []
    for model in models:
        query = select(model).where(func.date(model.dttm) == selected_date.isoformat())
        data = await session.scalars(query)
        result.append(data.all())
    return result


async def get_all(session: AsyncSession, table):
    query = select(table)
    result = await session.scalars(query)
    return result.all()
