import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as ticker
# Import seaborn
import seaborn as sns
from scipy import stats

df = pd.read_csv('Data/Characteristics/shared_messages_delay_group_by_with.csv')
print(df.dtypes)
print(df.head)
df['list_time_delay'] = df.list_time_delay.apply(lambda x: x[1:-1].split(','))
df = df.explode('list_time_delay', ignore_index=True)
df['list_time_delay'] = pd.to_numeric(df['list_time_delay'])
print(df)

sns.boxplot(
    data=df,
    x="host", y="list_time_delay", hue='shared_with'
)
plt.show()

ax = sns.boxplot(
    data=df,
    x="host", y="list_time_delay"
)
ax.set_xlabel("Host", size=12)
ax.set_ylabel("Delay [seconds]", size=12)
plt.show()