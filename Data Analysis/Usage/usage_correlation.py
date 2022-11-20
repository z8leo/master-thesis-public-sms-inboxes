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

sns.set_theme()

df_lu = pd.read_csv('Data/Characteristics/lifetime_uptime.csv')
print(df_lu.dtypes)
print(df_lu.head)

df_mc = pd.read_csv('Data/Characteristics/host_inbox_messagecount.csv')

df = df_lu.merge(df_mc)
print(df)
print(df.groupby('host')[['lifetime','uptime','message_count']].corr(method='pearson'))
all_corr = df.corr(method='pearson')
print(f'All correlation {all_corr}')

#Subplot
fig, ax = plt.subplots(1, 2, sharey=True, figsize=(14,5))

# Correlation Message - Lifetime
sns.scatterplot(df, x='lifetime', y='message_count', hue='host', ax=ax[0], legend=False)
ax[0].set_xlabel("Lifetime", size=12)
ax[0].set_ylabel("# Messages", size=12)

# Correlation Messages - Uptime
sns.scatterplot(df, x='uptime', y='message_count', hue='host', ax=ax[1], legend=False)
ax[1].set_xlabel("Uptime", size=12)
ax[1].set_ylabel("# Messages", size=12)
plt.show()