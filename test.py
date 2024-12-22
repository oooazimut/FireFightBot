import asyncio

# from pymodbus.client import AsyncModbusTcpClient
# from config import NetData
# # from service.modbus import ModbusService


# async def main():
#     client = AsyncModbusTcpClient(host=NetData.remote_host, port=NetData.remote_port)
#     await client.connect()
#     print(client.connected)
#     data = await client.read_holding_registers(16386, count=2)
#     if data:
#         data = client.convert_from_registers(
#             data.registers[::-1],
#             data_type=client.DATATYPE.FLOAT32,
#         )
#         print(round(data, 3))
#     # await ModbusService.client.connect()
#     # print(ModbusService.client.connected)


# if __name__ == "__main__":
#     asyncio.run(main())


from sqlalchemy import select 
from sqlalchemy.ext.asyncio import create_async_engine
from db.models import User
from config import settings


async def db_connection():
    engine = create_async_engine(settings.sqlite_async_dsn, echo=True)
    async with engine.begin() as conn:
        stmt = select(User)
        res = await conn.execute(stmt)
        print(res)


asyncio.run(db_connection())
