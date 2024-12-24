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
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from db.models import User, WaterLevel
from config import settings
from jobs import poll_and_save


async def db_connection():
    engine = create_async_engine(settings.sqlite_async_dsn, echo=True)
    db_pool = async_sessionmaker(engine)
    async with db_pool() as session:
        stmt = select(WaterLevel).order_by(WaterLevel.id.desc()).limit(1)
        curr_level = await session.scalar(stmt)



asyncio.run(db_connection())
