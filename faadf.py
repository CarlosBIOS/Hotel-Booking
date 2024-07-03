import pandas as pd

print(pd.read_csv('hotels.csv').loc[pd.read_csv('hotels.csv')['id'] == 134]['name'].squeeze())
