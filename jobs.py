from pymodbus.client import AsyncModbusTcpClient, ModbusBaseClient

from config import settings
from service.modbus import poll_registers


client: ModbusBaseClient = AsyncModbusTcpClient(
    settings.modbus.host,
    port=settings.modbus.port,
)

async def poll_and_save():
    rr = await poll_registers(client, 16386, 3)
    if rr:
        pass
