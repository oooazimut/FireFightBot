import logging
from aiogram.client.bot import Bot
from aiogram.exceptions import TelegramForbiddenError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio.session import AsyncSession
from db.models import User
from db.repo import get_all

logger = logging.getLogger(__name__)


async def started_pump_notification(bot: Bot, session: AsyncSession):
    users = await get_all(session, User)
    for user in users:
        try:
            await bot.send_message(user.id, "Запущен пожарный насос!")
        except ValidationError:
            pass
        except TelegramForbiddenError as errr:
            logger.error(f"Ошибка отправки: {str(errr)}")
