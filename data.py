import pandas as pd

df = pd.read_csv('population.csv')

countries = df['Entity'].unique().tolist()
min_year = int(df['Year'].unique().min())
max_year = int(df['Year'].unique().max())