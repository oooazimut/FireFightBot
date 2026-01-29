import functools
from pymodbus import ModbusException
from redis.asyncio import Redis

from infra.receiver.modbus.mapping import to_json


redis = Redis()


def cashe_to_redis(key: str = "modbus:latest"):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                await redis.set(key, to_json(result))
                return result
            except (ModbusException, ConnectionError):
                await redis.delete(key)

        return wrapper

    return decorator
