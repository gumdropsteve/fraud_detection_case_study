import pandas as pd

df = pd.read_json('data/data.json')

df['fraud'] = df['acct_type'].apply(lambda x: x[:5]) == 'fraud'
