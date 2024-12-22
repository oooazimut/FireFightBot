import logging

from pymodbus import ModbusException, pymodbus_apply_logging_config
from pymodbus.client import ModbusBaseClient

logger = logging.getLogger(__name__)


async def poll_registers(client: ModbusBaseClient, address, count) -> list | None:
    pymodbus_apply_logging_config(logging.WARNING)
    await client.connect()
    assert client.connected, "Нет соединения с ПР-103"
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
