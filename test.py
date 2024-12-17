import asyncio

from pymodbus.client import AsyncModbusTcpClient
from config import NetData
# from service.modbus import ModbusService


async def main():
    client = AsyncModbusTcpClient(host=NetData.remote_host, port=NetData.remote_port)
    await client.connect()
    print(client.connected)
    data = await client.read_holding_registers(16384)
    if data:
        print(data.registers)
    # await ModbusService.client.connect()
    # print(ModbusService.client.connected)


if __name__ == "__main__":
    asyncio.run(main())
