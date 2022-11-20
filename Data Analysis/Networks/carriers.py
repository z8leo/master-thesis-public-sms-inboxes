
import string
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Apply the default seaborn plot theme
sns.set_theme()

# Define datatypes
dtypes = {'number':str, 'mccmnc': str, 'mcc': str, 'mnc': str, 'msisdn': str, 'mccmnc': str, 'mcc': str, 'mnc': str, 'imsi': str, 'msin': str, 'original_country_prefix': str, 'is_ported': str, 'ported_country_prefix': str, 'is_roaming': str, 'roaming_country_prefix': str}
# Load datasets
raw_nt = pd.read_json('Data Collection/Third-Party APIs/nt_lookup/hlr_llokups_nt_20220920_115342.json', dtype=dtypes, encoding_errors='ignore')

print(f'Raw Number Type: {raw_nt}')

raw_hlr_1 = pd.read_json('Data Collection\Third-Party APIs\hlr_lookup\hlr_llokups_hlr_20220920_170520.json', dtype=dtypes)
raw_hlr_2 = pd.read_json('Data Collection\Third-Party APIs\hlr_lookup\hlr_llokups_hlr_20220920_160812.json', dtype=dtypes)

# Concat the HLR datasets
raw_hlr_combined = pd.concat([raw_hlr_1, raw_hlr_2], ignore_index=True)
print(f'Raw HLR combined: {raw_hlr_combined}')

# Left Join NT lookups with HLR lookups. Not every NT entry has HLR entry.
df = raw_nt.merge(raw_hlr_combined, left_on='number', right_on='msisdn', how='left', suffixes=['_nt', '_hlr'])

# Rows should be the same as the number of distinct phone numbers
print('Final dataset:')
print(df)
print(f'Datatypes: {df.dtypes}')


# Explore the date

# Validate 
print('Check for number != msiisdn')
print(df[['number', 'msisdn']].loc[(df['number'] != df['msisdn']) & (~df['msisdn'].isna())])

# Number type
sns.set(rc={"figure.figsize":(6, 6)}) #width=3, #height=4
ax = sns.countplot(df['number_type'], x=df['number_type'])
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
ax.set_xlabel('Line type')
ax.set_ylabel('Occurences')
ax.bar_label(ax.containers[0])
plt.tight_layout()
plt.show()

# How many number are ported?
print(f'Count ported: \n {df.is_ported.value_counts()}')
# How many ported networks?
print(f'Ported networks \n {df.ported_network_name.count()}')

# How many numbers are roaming
print(f'Count roaming: \n {df.is_roaming.value_counts()}')

# How many numbers are online?
print(f'Connectivity status: \n {df.connectivity_status.value_counts()}')

# Where numbers are ported, what are the original and ported networks?


# Connectivity status
sns.set(rc={"figure.figsize":(10, 10)}) #width=3, #height=4
ax = sns.countplot(df['connectivity_status'], x=df['connectivity_status'])
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
ax.set_xlabel('Connectivity status')
ax.set_ylabel('Occurences')
ax.bar_label(ax.containers[0])
plt.tight_layout()
plt.show()

# Original Networks
# Only show top 30 networks
sns.set(rc={"figure.figsize":(6, 6)}) #width=3, #height=4
ax = sns.countplot(df['original_network_name_hlr'], x=df['original_network_name_hlr'], hue=df['is_ported'], order=df['original_network_name_hlr'].value_counts().iloc[:10].index)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
ax.set_xlabel('Original Network')
ax.set_ylabel('Occurences')
ax.bar_label(ax.containers[0])
ax.bar_label(ax.containers[1])
plt.tight_layout()
plt.show()

# Ported network names
sns.set(rc={"figure.figsize":(14, 25)}) #width=3, #height=4
ax = sns.countplot(df['ported_network_name'], x=df['ported_network_name'], order=df['ported_network_name'].value_counts().iloc[:10].index)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
ax.set_xlabel('Ported Network names')
ax.set_ylabel('Occurences')
ax.bar_label(ax.containers[0])
plt.tight_layout()
plt.show()

# Serving Network names
# When a number is ported, the serving network is 'ported_network_name'
sns.set(rc={"figure.figsize":(14, 25)}) #width=3, #height=4
# Build Dataframe, when is_ported -> ported network name, else original_network_name
df['network'] = df['original_network_name_hlr'].mask(df['is_ported'] == 'True', other=df['ported_network_name'])
print(df['original_network_name_nt'].value_counts())
print(df['original_network_name_hlr'].value_counts())
print(df['ported_network_name'].value_counts())
print(df['is_ported'])
print(df['network'].value_counts())

ax = sns.countplot(df['network'], x=df['network'], order=df['network'].value_counts().iloc[:50].index)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
ax.set_xlabel('Serving Network names')
ax.set_ylabel('Occurences')
ax.bar_label(ax.containers[0])
plt.tight_layout()
plt.show()

# Where are they roaming?
sns.set(rc={"figure.figsize":(14, 25)}) #width=3, #height=4
# Build Dataframe, when is_ported -> ported network name, else original_network_name
df_roaming = df[['roaming_country_name', 'roaming_network_name']].mask(df['is_roaming'] == True)
ax = sns.countplot(df_roaming['roaming_network_name'], x=df_roaming['roaming_network_name'], order=df_roaming['roaming_network_name'].value_counts().iloc[:50].index)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
ax.set_xlabel('Roaming networrks')
ax.set_ylabel('Occurences')
ax.bar_label(ax.containers[0])
plt.tight_layout()
plt.show()

# Countries
sns.set(rc={"figure.figsize":(14, 25)}) #width=3, #height=4
# Build Dataframe, when is_ported -> ported network name, else original_network_name
ax = sns.countplot(df['original_country_name_hlr'], x=df['original_country_name_hlr'], order=df['original_country_name_hlr'].value_counts().index)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
ax.set_xlabel('Countries')
ax.set_ylabel('Occurences')
ax.bar_label(ax.containers[0])
plt.tight_layout()
plt.show()

# Which carriers do take number offline? Highest (Absent+Connected vs Undetermined+Invalid ratio)
sns.set(rc={"figure.figsize":(14, 25)}) #width=3, #height=4
df['is_online'] = df['connectivity_status'].replace(['ABSENT', 'CONNECTED'], True).replace(['UNDETERMINED', 'INVALID_MSISDN'], False)
ax = sns.countplot(df['network'], x=df['network'], hue=df['is_online'], order=df['network'].value_counts().iloc[:30].index)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
ax.set_xlabel('Serving Network')
ax.set_ylabel('Occurences')
ax.bar_label(ax.containers[0])
ax.bar_label(ax.containers[1])
plt.tight_layout()
plt.show()