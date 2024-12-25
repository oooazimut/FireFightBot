from matplotlib.axes import Axes
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def plot_current_level(level: int | float, pump: bool, pressure: float):
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

    def draw_pressure(axes: Axes, pressure: float, pump: bool):
        if pump or pressure > 0.4:
            axes.text()
        else:
            axes.text()

    plt.clf()
    fig, axes = plt.subplots()
    img = np.asarray(Image.open("media/curr_bg.png"))
    axes.imshow(img)
    draw_water(axes, level)
    plt.savefig("media/current_level.png")
