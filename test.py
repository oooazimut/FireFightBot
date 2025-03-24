import sqlite3 as sq
from datetime import datetime  # noqa: F401

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

query = 'select * from pressures where value > 0 and DATE(dttm) = DATE("now")'
with sq.connect(
    "FireFight.db", detect_types=sq.PARSE_COLNAMES | sq.PARSE_DECLTYPES
) as con:
    result = con.execute(query).fetchall()


dttms = [datetime.strptime(i[2], '%Y-%m-%d %H:%M:%S.%f') for i in result]
pressures = [i[1] for i in result]


def draw_plot(xdata, ydata, title, axes: Axes, max_ylimit):
    x_values = np.array(xdata)
    y_values = np.array(ydata)
    axes.set_ylim(0, max_ylimit)
    axes.grid()
    axes.set_title(title)
    axes.plot(x_values, y_values)


date_format = mdates.DateFormatter("%H:%M:%S")

plt.clf()
fig, ax = plt.subplots(1, 1)
ax.xaxis.set_major_formatter(date_format)
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
draw_plot(dttms, pressures, "Давление воды в системе", ax, 7)
fig.autofmt_xdate()
fig.savefig("media/давление.png")
plt.close(fig)
