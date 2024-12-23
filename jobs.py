import logging

from pymodbus.client import ModbusBaseClient
from sqlalchemy.orm import sessionmaker

from db.models import Pressure, WaterLevel
from service.modbus import poll_registers

logger = logging.getLogger(__name__)


async def poll_and_save(client: ModbusBaseClient, db_pool: sessionmaker):
    rr = await poll_registers(client, 16384, 4)
    if rr:
        water_level = WaterLevel(value=rr[0])
        temp = rr[2::]
        temp.reverse()
        pressure = Pressure(
            value=client.convert_from_registers(
                temp, data_type=client.DATATYPE.FLOAT32
            ),
        )
        async with db_pool() as session:
            session.add_all([pressure, water_level])
            await session.commit()
    else:
        logger.error("Не получены данные по модбас!")
