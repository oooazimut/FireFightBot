import logging

from pymodbus import ModbusException
from pymodbus.client import ModbusBaseClient

logger = logging.getLogger(__name__)


async def poll_registers(client: ModbusBaseClient, address, count) -> list | None:
    await client.connect()
    if not client.connected:
        logger.error("Нет соединения с ПР-103")
        client.close()
        return
    try:
        data = await client.read_holding_registers(address, count=count)
    except ModbusException as exc:
        logger.error(f"Ошибка протокола Modbus: {exc}")
        client.close()
        return
    if data.isError():
        logger.error(f"Чтение регистров завершилось ошибкой: {data}")
        client.close()
        return
    client.close()
    return data.registers
