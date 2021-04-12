import pandas as pd
import datetime

df = pd.read_csv('population.csv')

countries = df['Entity'].unique().tolist()
min_year = int(df['Year'].unique().min())
max_year = int(df['Year'].unique().max())

# Limits of the data

CURRENCIES = ['BTC', 'DASH', 'ETC', 'ETH', 'OMG', 'LTC', 'NEO', 'XMR']

MIN_DATE = datetime.date(2015, 10, 8)
MAX_DATE = datetime.date(2021, 4, 6)