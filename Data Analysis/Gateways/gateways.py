import csv
from random import seed
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns

# Read araxxe results
df = pd.read_csv('Data/Characteristics/araxxe_results.csv', dtype={'number': str})
print(df.dtypes)
print(df)

# Read numbers per provider
df_host = pd.read_csv('Data/Characteristics/numbers_per_provider_2022_09_22.csv')
print(df_host.dtypes)
print(df_host)

# Result datafram
df_result = pd.DataFrame({'host': [], 'count': [], 'total': []})

# Iterate through hosts and find which of their numbers flagged as SIM box
for index, row in df_host.iterrows():
    # Count how many SIm Box numbers
    count = 0
    for j, srow in df.iterrows():
        if srow['number'] in row['numbers']:
            count += 1
    # Add row to result df
    df_result.loc[index,:] = [row['host'], count, row['total']]

print(f'Hosts with SIM box numbers: \n {df_result}')

# Which networks?



# Define datatypes
dtypes = {'number':str, 'mccmnc': str, 'mcc': str, 'mnc': str, 'msisdn': str, 'mccmnc': str, 'mcc': str, 'mnc': str, 'imsi': str, 'msin': str, 'original_country_prefix': str, 'is_ported': str, 'ported_country_prefix': str, 'is_roaming': str, 'roaming_country_prefix': str}
# Load datasets
raw_nt = pd.read_json('Data Collection\Third-Party APIs\hlr_llokups_nt_20220920_115342.json', dtype=dtypes)
print(f'Raw Number Type: {raw_nt}')

raw_hlr_1 = pd.read_json('Data Collection\Third-Party APIs\hlr_llokups_hlr_20220920_170520.json', dtype=dtypes)
raw_hlr_2 = pd.read_json('Data Collection\Third-Party APIs\hlr_llokups_hlr_20220920_160812.json', dtype=dtypes)

# Concat the HLR datasets
raw_hlr_combined = pd.concat([raw_hlr_1, raw_hlr_2], ignore_index=True)
print(f'Raw HLR combined: {raw_hlr_combined}')

# Left Join NT lookups with HLR lookups. Not every NT entry has HLR entry.
df_networks = raw_nt.merge(raw_hlr_combined, left_on='number', right_on='msisdn', how='left', suffixes=['_nt', '_hlr'])

# Boolean value if sim box number for all numbers
df['simbox'] = True
print(df)

# Left join networks and SIM box numbers and 
df_networks = df_networks.merge(df, left_on='number', right_on='number', how='left', suffixes=['_nt', '_sb'])

print(f'Final dataset: \n {df_networks} \n {df_networks.dtypes}')
print(f'Count number {df_networks.simbox.value_counts()}')

# Apply the default seaborn plot theme
sns.set_theme()

# Plot networks
# Serving Network names
# When a number is ported, the serving network is 'ported_network_name'
sns.set(rc={"figure.figsize":(14, 25)}) #width=3, #height=4
# Build Dataframe, when is_ported -> ported network name, else original_network_name
df_networks['network'] = df_networks['original_network_name_hlr'].mask(df_networks['is_ported'] == 'True', other=df_networks['ported_network_name'])
ax = sns.countplot(df_networks['network'], x=df_networks['network'], hue=df_networks['simbox'], order=df_networks['network'].value_counts().iloc[:].index)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
ax.set_xlabel('Serving Network names')
ax.set_ylabel('Occurences')
ax.bar_label(ax.containers[0])
plt.tight_layout()
plt.show()