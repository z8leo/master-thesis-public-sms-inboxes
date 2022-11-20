import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np

df = pd.read_csv('Data/Providers/providers.csv')
# Convert tranco rank to integer
df['trancoRank'] = df['trancoRank'].fillna(0).astype(int)
# Convert Monetization to List
df['monetization'] = df['monetization'].apply(lambda l: l.split())

print(df.head)


# Top 20 most popular sites according to tranco list
df.sort_values(by=['trancoRank'], inplace=True)     # Sort
topTen = df[df['trancoRank'] > 0].iloc[:20]         # Filter out rank 0 (NA), slice first 10 entries
print(topTen[['host', 'trancoRank']])


# Monetization
# List to one Dimension, from https://towardsdatascience.com/dealing-with-list-values-in-pandas-dataframes-a177e534f173
def to_1D(series):
 return pd.Series([x for _list in series for x in _list])

print(to_1D(df['monetization']).value_counts())

# Barplot percentage of monetization types
fig, ax = plt.subplots(figsize = (14,4))
ax.bar(to_1D(df['monetization']).value_counts().index, to_1D(df['monetization']).value_counts(normalize=True).values*100)
ax.set_ylabel("Frequency [%]", size = 12)
ax.set_title("Montetization types", size = 14)
plt.show()

# How many do have privacy policy?
print(df['privacy'])
dfPrivacyExists = df['privacy'].mask(cond=df['privacy'] == 'None', other='False').mask(cond=df['privacy'] != 'None', other='True')
print(dfPrivacyExists.value_counts())
# Barplot percentage of privacy policies
fig, ax = plt.subplots(figsize = (14,4))
ax.bar(dfPrivacyExists.value_counts().index, dfPrivacyExists.value_counts(normalize=True).values*100)
ax.set_ylabel("Frequency [%]", size = 12)
ax.set_title("Privacy policy exist?", size = 14)
plt.show()

# How many do have TOS?
print(df['tos'])
dfPrivacyExists = df['tos'].mask(cond=df['tos'] == 'None', other='False').mask(cond=df['tos'] != 'None', other='True')
print(dfPrivacyExists.value_counts())
# Barplot percentage of privacy policies
fig, ax = plt.subplots(figsize = (14,4))
ax.bar(dfPrivacyExists.value_counts().index, dfPrivacyExists.value_counts(normalize=True).values*100)
ax.set_ylabel("Frequency [%]", size = 12)
ax.set_title("ToS exist?", size = 14)
plt.show()

