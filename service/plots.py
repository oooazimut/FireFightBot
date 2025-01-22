from datetime import date, timedelta
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from PIL import Image
from sqlalchemy import Sequence

from db.models import Pressure, WaterLevel


def plot_current_level(level: int | float, pump: int, pressure: float):
    pressure = 0 if pressure <= 0 else pressure

    def draw_water(axes: Axes, level: int | float):
        width = 467
        level *= 2.8
        y_start_point = 530 - level
        water = Rectangle(
            xy=(80, y_start_point),
            width=width,
            height=level,
            facecolor="skyblue",
        )
        axes.add_patch(water)

    def top_text(axes: Axes, pump: int):
        if not pump:
            return

        s = "работает насос!"
        if pump > 1:
            s += "\nнизкое давление!"
        axes.text(100, 150, s, fontsize=30, color="red")

    plt.clf()
    fig, axes = plt.subplots()
    img = np.asarray(Image.open("media/curr_bg.png"))
    axes.imshow(img)
    draw_water(axes, level)
    axes.text(600, 350, f"давление:\n{round(pressure, 2)} бар", fontsize=20)
    top_text(axes, pump)
    plt.title("Текущий уровень воды в пожарной емкости", fontsize=15)
    plt.xticks([])
    plt.yticks([])
    fig.savefig("media/current_level.png")
    plt.close(fig)


def plot_archive_levels(
    levels: Sequence[WaterLevel],
    pressures: Sequence[Pressure],
    clicked_date: date,
):
    interval = clicked_date - timedelta(days=7)
    x_levels = np.array([level.dttm for level in levels])
    y_levels = np.array([level.value for level in levels])

    x_pressures = np.array([pressure.dttm for pressure in pressures])
    y_pressures = np.array([
        0 if pressure.value <= 0 else pressure.value for pressure in pressures
    ])

    fig, axes = plt.subplots(2, 1, sharex=True)
    fig.suptitle(f"{interval.isoformat()} - {clicked_date.isoformat()}")
    date_format = mdates.DateFormatter("%m.%d")
    axes[1].xaxis.set_major_formatter(date_format)
    axes[0].set_ylim(0, 110)
    axes[1].set_ylim(0, 7)
    axes[0].set_title("Уровень воды в емкости")
    axes[1].set_title("Давление воды в системе")
    axes[0].grid()
    axes[1].grid()

    axes[0].plot(x_levels, y_levels)
    axes[1].plot(x_pressures, y_pressures)
    fig.savefig("media/archive_data.png")
    plt.close(fig)
