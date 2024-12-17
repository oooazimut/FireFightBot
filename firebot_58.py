import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from redis.asyncio import Redis

from config import TOKEN
from custom.media_storage import MediaIdStorage


async def main():
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    storage = RedisStorage(
        Redis(),
        key_builder=DefaultKeyBuilder(
            with_destiny=True,
            with_bot_id=True,
        ),
    )
    dp = Dispatcher(storage=storage)
    setup_dialogs(dp, media_id_storage=MediaIdStorage())
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
