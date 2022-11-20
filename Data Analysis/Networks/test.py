import pandas as pd

a = pd.Series([1, 2, 3])
b = pd.Series([0, 0, 0])
c = pd.Series([False, True, False])
df = pd.DataFrame({'a': a, 'b': b, 'c': c})
print(df)
df['a'] = df['a'].mask(df['c'] == True, other=df['b'])
print(df)