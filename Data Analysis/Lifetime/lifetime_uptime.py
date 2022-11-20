import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as ticker
# Import seaborn
import seaborn as sns
from scipy import stats

df = pd.read_csv('Data/Characteristics/lifetime_uptime.csv')
print(df.dtypes)
print(df.head)

sns.set_theme()

fig, ax = plt.subplots(1, 2, sharey=True, figsize=(14,5))

sns.ecdfplot(df, x="lifetime", hue="host", ax=ax[0], legend=False)
ax[0].set_xlabel("Lifetime [days]", size=12)

sns.ecdfplot(df, x="uptime", hue="host", ax=ax[1], legend=True)
ax[1].set_xlabel("Uptime [days]", size=12)

sns.move_legend(ax[1], "upper left", bbox_to_anchor=(1, 1))
plt.show()

# Correlation with amount of messages
df_b = pd.read_csv('Data/Characteristics/host_inbox_messagecount.csv')
print(df_b)
df_merged = df.merge(df_b, how='left', on=['host', 'message_number'])
print(df_merged)

sns.relplot(data=df_merged, x="lifetime", y="message_count", hue="host")
plt.show()