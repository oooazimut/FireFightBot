from datetime import date, datetime, timedelta

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedCalendar
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from config import settings
from db.models import Pressure, PumpCondition, User, WaterLevel
from db.repo import get_by_date, get_last
from service.plots import plot_archive_levels, plot_current_level
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
    curr_level = await get_last(session, [WaterLevel])
    curr_level = curr_level[0]

    if not curr_level or curr_level.dttm < datetime.now() - timedelta(minutes=5):
        await callback.answer("Нет свежих данных", show_alert=True)
        return

    if 100 >= curr_level.value >= 0:
        pump_condition, pressure = await get_last(session, [PumpCondition, Pressure])

        plot_current_level(
            level=curr_level.value,
            pump=pump_condition.condition,
            pressure=pressure.value,
        )
        await manager.switch_to(MainSG.curr_level)
    else:
        await callback.answer("Датчик неисправен!", show_alert=True)


async def on_date_clicked(
    callback: CallbackQuery,
    widget: ManagedCalendar,
    manager: DialogManager,
    clicked_date: date,
    /,
):
    session: AsyncSession = manager.middleware_data["session"]
    levels, pressures = await get_by_date(session, clicked_date, [WaterLevel, Pressure])

    if levels or pressures:
        plot_archive_levels(levels, pressures, clicked_date)
        await manager.switch_to(MainSG.archive)
    else:
        await callback.answer("Данных нет", show_alert=True)
