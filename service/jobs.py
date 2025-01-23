import logging

from aiogram.client.bot import Bot
from pymodbus.client import ModbusBaseClient
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from db.models import Pressure, PumpCondition, WaterLevel
from db.repo import get_last
from service.notifications import started_pump_notification
from .modbus import poll_registers

logger = logging.getLogger(__name__)


async def check_pump(bot: Bot, session: AsyncSession, pump_condition: int):
    if not pump_condition:
        return
    prev_condition = await get_last(session, [PumpCondition])
    if not prev_condition[0].condition:
        await started_pump_notification(bot, session)


async def poll_and_save(db_pool: sessionmaker, bot: Bot):
    rr = await poll_registers(16384, 5)
    if rr:
        water_level = WaterLevel(value=rr["water_level"])
        pump_condition = PumpCondition(condition=rr["pump_condition"])
        data = [water_level, pump_condition]
        if rr['pressure'] > 0:
            pressure = Pressure(value=rr["pressure"])
            data.append(pressure)

        async with db_pool() as session:
            await check_pump(bot, session, pump_condition.condition)
            session.add_all(data)
            await session.commit()
    else:
        logger.error("Не получены данные по модбас!")
