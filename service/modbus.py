import logging

from pymodbus import ExceptionResponse, ModbusException
from pymodbus.client import AsyncModbusTcpClient, ModbusBaseClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder

from config import NetData

logger = logging.getLogger(__name__)


class ModbusService:
    client: ModbusBaseClient = AsyncModbusTcpClient(
        host=NetData.remote_host,
        port=NetData.remote_port,
    )
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)

    @classmethod
    async def write_float(cls, register, value):
        cls.builder.add_32bit_float(value)
        payload = cls.builder.build()
        await cls.client.write_registers(
            address=register,
            values=payload,
            slave=16,
            # skip_encode=True,
        )

    @classmethod
    def convert_to_float(cls, registers: list) -> float:
        decoder = BinaryPayloadDecoder.fromRegisters(
            registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE
        )
        result = decoder.decode_32bit_float()
        return result

    @classmethod
    async def polling(cls, address, count) -> list | None:
        await cls.client.connect()
        assert cls.client.connected, "Нет соединения с ПР-103"
        try:
            data = await cls.client.read_holding_registers(address, count=count)
        except ModbusException as exc:
            logger.error(f"1 {exc}")
            cls.client.close()
            return
        if data.isError():
            logger.error(data)
            cls.client.close()
            return
        if isinstance(data, ExceptionResponse):
            logger.error(f" 2 {data}")
            cls.client.close()
            return
        cls.client.close()
        return data.registers
