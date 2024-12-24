from datetime import datetime, timedelta

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.kbd import ManagedCalendar
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from config import settings
from db.models import User, WaterLevel
from service.plots import plot_current_level
from states import MainSG


async def check_passwd(msg: Message, msg_inpt, manager: DialogManager):
    if msg.text == settings.password.get_secret_value():
        session: AsyncSession = manager.middleware_data["session"]
        session.add(User(id=msg.from_user.id, name=msg.from_user.full_name))
        await session.commit()
        await manager.next()
    else:
        await msg.answer("Неверно, попробуйте ещё раз")


async def on_current_level(callback: CallbackQuery, button, manager: DialogManager):
    session: AsyncSession = manager.middleware_data["session"]
    query = select(WaterLevel).order_by(WaterLevel.id.desc()).limit(1)
    curr_level = await session.scalar(query)

    if not curr_level or curr_level.dttm < datetime.now() - timedelta(minutes=5):
        await callback.answer("Нет свежих данных", show_alert=True)
        return

    if 100 >= curr_level.value >= 0:
        plot_current_level(level=curr_level.value)
        await manager.switch_to(MainSG.curr_level)
    else:
        await callback.answer("Датчик неисправен!", show_alert=True)


async def on_date_clicked(
    callback: ChatEvent,
    widget: ManagedCalendar,
    manager: DialogManager,
    clicked_date: datetime.date,
    /,
):
    pass