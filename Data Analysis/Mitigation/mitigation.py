import string
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Apply the default seaborn plot theme
sns.set_theme()

# Define datatypes
#dtypes = {'number':str, 'mccmnc': str, 'mcc': str, 'mnc': str, 'msisdn': str, 'mccmnc': str, 'mcc': str, 'mnc': str, 'imsi': str, 'msin': str, 'original_country_prefix': str, 'is_ported': str, 'ported_country_prefix': str, 'is_roaming': str, 'roaming_country_prefix': str}
# Load datasets
df = pd.read_json('Data Collection\Third-Party APIs\phone_reputation\ipqualityscore_results_20221027_101155.json')
print(df)

df = df.drop(39)
df = df[['fraud_score', 'recent_abuse', 'risky', 'active']]
print(df)

print(df.value_counts())