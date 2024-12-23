import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from pymodbus.client import AsyncModbusTcpClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import settings
from custom.media_storage import MediaIdStorage
from middlewares import DbSessionMiddleware
from jobs import poll_and_save


async def main():
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    engine = create_async_engine(settings.sqlite_async_dsn, echo=True)
    db_pool = async_sessionmaker(engine, expire_on_commit=False)
    client = AsyncModbusTcpClient(
        settings.modbus.host,
        port=settings.modbus.port,
    )
    scheduler = AsyncIOScheduler()
    scheduler.start()
    scheduler.add_job(
        poll_and_save,
        trigger="interval",
        seconds=15,
        id="polling",
        args=[client, db_pool],
    )

    bot = Bot(
        token=settings.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    storage = RedisStorage(
        Redis(),
        key_builder=DefaultKeyBuilder(
            with_destiny=True,
            with_bot_id=True,
        ),
    )
    dp = Dispatcher(storage=storage)
    setup_dialogs(dp, media_id_storage=MediaIdStorage())
    dp.update.outer_middleware(DbSessionMiddleware(db_pool))

    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
