from datetime import date, datetime, timedelta

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.kbd import ManagedCalendar
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from config import settings
from db.models import Pressure, PumpCondition, User, WaterLevel
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
    query = select(WaterLevel).order_by(WaterLevel.id.desc()).limit(1)
    curr_level = await session.scalar(query)

    if not curr_level or curr_level.dttm < datetime.now() - timedelta(minutes=5):
        await callback.answer("Нет свежих данных", show_alert=True)
        return

    if 100 >= curr_level.value >= 0:
        query = select(PumpCondition).order_by(PumpCondition.id.desc()).limit(1)
        pump_condition = await session.scalar(query)
        query = select(Pressure).order_by(Pressure.id.desc()).limit(1)
        pressure = await session.scalar(query)

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
    query = select(WaterLevel).where(func.date(WaterLevel.dttm) == clicked_date.isoformat())
    levels = await session.scalars(query)
    levels = levels.all()
    query = select(Pressure).where(func.date(Pressure.dttm) == clicked_date.isoformat())
    pressures = await session.scalars(query)
    pressures = pressures.all()

    if levels or pressures:
        plot_archive_levels(levels, pressures, clicked_date)
        await manager.switch_to(MainSG.archive)
    else:
        await callback.answer('Данных нет', show_alert=True)
    
