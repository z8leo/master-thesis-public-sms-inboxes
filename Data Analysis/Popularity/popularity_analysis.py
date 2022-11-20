import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as ticker
# Import seaborn
import seaborn as sns
from scipy import stats

df = pd.read_csv('Data/Characteristics/messages_inboxes_per_host.csv')
print(df.dtypes)
print(df.head)

dfb = pd.read_csv('Data/Providers/providers.csv')
# Convert tranco rank to integer. Fill NA with rank 1,000,000
dfb['trancoRank'] = dfb['trancoRank'].fillna(1000000).astype(int)
# Only subset of variables needed
dfb = dfb[['trancoRank', 'host']]
print(dfb.dtypes)
print(dfb.head)

# Merge dataframes
df = df.merge(dfb, how='left', on='host')
# Sort
df = df.sort_values(by=['trancoRank'])
print(df.head)

#corrTrancoMessages = df.corr(method='pearson')
#print(corrTrancoMessages)

# Calculate pearson correlation
rm = stats.pearsonr(df['trancoRank'], df['message_count'])
print(rm)
ri = stats.pearsonr(df['trancoRank'], df['inbox_count'])
print(ri)


# Apply the default theme
sns.set_theme()

# Two sublplots
fig, ax = plt.subplots(1, 2, sharey=True, figsize=(14,5))

# Create scatterplot message count ~ tranco rank
sns.scatterplot(
    data=df,
    x="message_count", y="trancoRank", hue='host', legend=False, ax=ax[0]
)

ax[0].set_ylabel("Tranco Rank [log]", size=12)
ax[0].set_xlabel("Number of messages", size=12)
plt.suptitle("Correlation between Tranco rank, Inbox count and Messsage count", size=14)
##ax.set_xticks(x)
ax[0].xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
ax[0].yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
ax[0].invert_yaxis()
plt.yscale('log')

sns.scatterplot(
    data=df,
    x="inbox_count", y="trancoRank", hue='host', legend=True, ax=ax[1]
)
ax[1].set_xlabel("Number of inboxes", size=12)
plt.show()
