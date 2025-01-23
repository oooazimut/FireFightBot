from datetime import date, timedelta
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from PIL import Image


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
    levels,
    pressures,
    clicked_date: date,
):
    def draw_plot(data, title, axes: Axes, max_ylimit):
        x_values = np.array([i.dttm for i in data])
        y_values = np.array([i.value for i in data])
        axes.set_ylim(0, max_ylimit)
        axes.grid()
        axes.set_title(title)
        axes.plot(x_values, y_values)

    interval = clicked_date - timedelta(days=7)
    date_format = mdates.DateFormatter("%m.%d")

    if pressures:
        fig, axes = plt.subplots(2, 1, sharex=True)
        axes[0].xaxis.set_major_formatter(date_format)
        draw_plot(levels, "Уровень воды в емкости", axes[0], 110)
        draw_plot(pressures, "Давление воды в системе", axes[1], 7)
    else:
        fig, ax = plt.subplots(1, 1)
        ax.xaxis.set_major_formatter(date_format)
        draw_plot(levels, "Уровень воды в емкости", ax, 110)
    
    fig.suptitle(f"{interval.isoformat()} - {clicked_date.isoformat()}")
    fig.savefig("media/archive_data.png")
    plt.close(fig)
