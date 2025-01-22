from datetime import date, timedelta
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
    interval = selected_date - timedelta(days=7)
    result = []
    for model in models:
        query = select(model).filter(func.date(model.dttm).between(interval, selected_date))
        data = await session.scalars(query)
        result.append(data.all())
    return result


async def get_all(session: AsyncSession, table):
    query = select(table)
    result = await session.scalars(query)
    return result.all()
