from datetime import date

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Calendar, CalendarScope
from aiogram_dialog.widgets.kbd.calendar_kbd import (
    DATE_TEXT,
    TODAY_TEXT,
    CalendarDaysView,
    CalendarMonthView,
    CalendarScopeView,
    CalendarYearsView,
)
from aiogram_dialog.widgets.text import Format, Text
from babel.dates import get_day_names, get_month_names

# class RuWeekDay(Text):
#     def __init__(self, locale):
#         super().__init__()
#         self.locale = locale

#     async def _render_text(self, data, manager: DialogManager) -> str:
#         selected_date: date = data["date"]
#         return get_day_names(width="short", context="stand-alone", locale=self.locale)[
#             selected_date.weekday()
#         ].title()


# class RuMonth(Text):
#     def __init__(self, locale):
#         super().__init__()
#         self.locale = locale

#     async def _render_text(self, data, manager: DialogManager) -> str:
#         selected_date: date = data["date"]
#         # print("month", selected_date.month)
#         return get_month_names("wide", context="stand-alone", locale=self.locale)[
#             selected_date.month
#         ].title()


# class CustomCalendar(Calendar):
#     def _init_views(self) -> Dict[CalendarScope, CalendarScopeView]:
#         return {
#             CalendarScope.DAYS: CalendarDaysView(
#                 self._item_callback_data,
#                 self.config,
#                 header_text=RuMonth("ru_RU"),
#                 weekday_text=RuWeekDay("ru_RU"),
#                 next_month_text=RuMonth("ru_RU") + " >>",
#                 prev_month_text="<< " + RuMonth("ru_RU"),
#             ),
#             CalendarScope.MONTHS: CalendarMonthView(
#                 self._item_callback_data,
#                 self.config,
#                 month_text=RuMonth("ru_RU"),
#                 this_month_text="[" + RuMonth("ru_RU") + "]",
#             ),
#             CalendarScope.YEARS: CalendarYearsView(
#                 self._item_callback_data,
#                 self.config,
#             ),
#         }


SELECTED_DAYS_KEY = "selected_dates"


class WeekDay(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        selected_date: date = data["date"]
        locale = manager.event.from_user.language_code
        return get_day_names(
            width="short",
            context="stand-alone",
            locale=locale,
        )[selected_date.weekday()].title()


class MarkedDay(Text):
    def __init__(self, mark: str, other: Text):
        super().__init__()
        self.mark = mark
        self.other = other

    async def _render_text(self, data, manager: DialogManager) -> str:
        current_date: date = data["date"]
        serial_date = current_date.isoformat()
        selected = manager.dialog_data.get(SELECTED_DAYS_KEY, [])
        if serial_date in selected:
            return self.mark
        return await self.other.render_text(data, manager)


class Month(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        selected_date: date = data["date"]
        locale = manager.event.from_user.language_code
        return get_month_names(
            "wide",
            context="stand-alone",
            locale=locale,
        )[selected_date.month].title()


class CustomCalendar(Calendar):
    def _init_views(self) -> dict[CalendarScope, CalendarScopeView]:
        return {
            CalendarScope.DAYS: CalendarDaysView(
                self._item_callback_data,
                date_text=MarkedDay("🔴", DATE_TEXT),
                today_text=MarkedDay("⭕", TODAY_TEXT),
                header_text="~~~~~ " + Month() + " ~~~~~",
                weekday_text=WeekDay(),
                next_month_text=Month() + " >>",
                prev_month_text="<< " + Month(),
            ),
            CalendarScope.MONTHS: CalendarMonthView(
                self._item_callback_data,
                month_text=Month(),
                header_text="~~~~~ " + Format("{date:%Y}") + " ~~~~~",
                this_month_text="[" + Month() + "]",
            ),
            CalendarScope.YEARS: CalendarYearsView(
                self._item_callback_data,
            ),
        }
