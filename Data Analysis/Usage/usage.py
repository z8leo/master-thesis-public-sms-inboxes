from operator import truediv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as ticker
# Import seaborn
import seaborn as sns
from scipy import stats
import matplotlib.dates as mdates 

parser = lambda date: pd.datetime.strptime(date, '%d-%m-%Y')
df = pd.read_csv('Data/Characteristics/us_pattern_days.csv', parse_dates=['day'], date_parser=parser)
print(df.dtypes)
print(df.head)

df_hour = pd.read_csv('Data/Characteristics/us_pattern_hour.csv')
print(df_hour.dtypes)
print(df_hour.head)

sns.set_theme()

plt.figure(figsize=(8.3, 3))
ax = sns.lineplot(df, x="day", y="count", hue="host", legend=False)
ax.set_ylabel("Messages", size=12)
ax.set_xlabel("Date", size=12)
myFmt = mdates.DateFormatter('%d.%m')
ax.xaxis.set_major_formatter(myFmt)
ax.xaxis.set_major_locator(ticker.MultipleLocator(7))
plt.show()

plt.figure(figsize=(6.3, 3))

ax = sns.lineplot(df_hour, x="hour", y="count", hue="host", legend=True, errorbar='sd')
ax.set_xlabel("Hour [UTC]", size=12)
ax.set_ylabel("Messages", size=12)

sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
plt.show()

