import asyncio
import functools
import logging
from typing import List
from pymodbus import ModbusException
from pymodbus.client import AsyncModbusTcpClient
from redis.asyncio import Redis

from domain.ports import Receiver
from infra.receiver.modbus.mapping import to_domain_model, to_json


ADDRESS = 16384
COUNT = 5

redis = Redis()
logger = logging.getLogger(__name__)


def cache_to_redis(key: str = "modbus:latest"):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                await redis.set(key, to_json(result))
                return result
            except (ModbusException, ConnectionError):
                await redis.delete(key)
                raise

        return wrapper

    return decorator


class ModbusReceiver(Receiver):
    def __init__(self, settings):
        self._client = AsyncModbusTcpClient(
            host=settings.host,
            port=settings.port,
        )
        self._lock = asyncio.Lock()

    async def _connect(self):
        if self._client.connected:
            return

        logger.info("Connect to ModbusDevice...")
        await self._client.connect()

        if not self._client.connected:
            logger.error("Connection doesn't exist, ConnectionError")
            raise ConnectionError("Can't connect to MbDevice")

    def _convert_to_float(self, words: List[int]):
        return self._client.convert_from_registers(
            words,
            data_type=self._client.DATATYPE.FLOAT32,
            word_order="little",
        )

    @cache_to_redis()
    async def receive(self):
        async with self._lock:
            await self._connect()
            try:
                rr = await self._client.read_holding_registers(
                    address=ADDRESS, count=COUNT
                )
                if rr.isError():
                    raise ModbusException(rr)
                return to_domain_model(rr.registers, self._convert_to_float)
            except ModbusException as e:
                logger.error(f"Modbus error: {e}")
                self._client.close()
                raise
