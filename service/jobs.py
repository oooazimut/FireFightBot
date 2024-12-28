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


async def poll_and_save(client: ModbusBaseClient, db_pool: sessionmaker, bot: Bot):
    rr = await poll_registers(client, 16384, 5)
    if rr:
        rr[0] = 100 if 200 > rr[0] > 100 else rr[0]
        water_level = WaterLevel(value=rr[0])
        temp = rr[2:4]
        temp.reverse()
        pressure = Pressure(
            value=client.convert_from_registers(
                temp, data_type=client.DATATYPE.FLOAT32
            ),
        )
        pump_condition = PumpCondition(condition=rr[-1])

        async with db_pool() as session:
            await check_pump(bot, session, pump_condition.condition)
            session.add_all([pressure, water_level, pump_condition])
            await session.commit()
    else:
        logger.error("Не получены данные по модбас!")
