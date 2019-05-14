"""
Set of functions that take the data.json data from the fraud case study in a Pandas dataframe form and return sanitized numerical dataframes
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML, display
import seaborn as sns


def max_data_pipeline(df_old):
    
    """
    Input: Fraud DataFrame with columns including:
    acct_type             14337 non-null object
    approx_payout_date    14337 non-null int64
    body_length           14337 non-null int64
    channels              14337 non-null int64
    country               14256 non-null object
    currency              14337 non-null object
    delivery_method       14321 non-null float64
    description           14337 non-null object
    email_domain          14337 non-null object
    event_created         14337 non-null int64
    event_end             14337 non-null int64
    
    Output: 
    Dataframe with columns:
    
    acct_type: Turned into 'fraud' column and dropped
    approx_payout_date: Dropped (correlates perfectly with event end)
    body_length: Unchanged
    channels: Dropped
    country: Dropped (too many categories) <-look at this later
    currency: Dropped (too many categories) <-look at this later
    delivery_method: Convert to one-hot (0,1,2,3)
    description: dropped (too many)
    email_domain: dropped (check out later)
    event_created: unchanged
    event_end: unchanged
    event_delay: event_end - event_created
    fraud: acct_type starts with fraud
    """
    
    #create copy
    df = df_old.copy()
    
    #create fraud column
    if 'acct_type' in df: 
        df['fraud'] = df['acct_type'].apply(lambda x: x[:5] == 'fraud').astype(int)
    
    #drop unused columns
    dropped_cols = ['name','approx_payout_date','channels','country','currency','description', 'email_domain']
    if 'acct_type' in df:
        dropped_cols.append('acct_type')
    df.drop(dropped_cols, inplace = True, axis = 1)
    
    #create event_delay
    df['event_delay'] = df['event_end'] - df['event_created']
    
    #One-hot encode 'delivery'
    df = pd.get_dummies(df, prefix = 'delivery', columns = ['delivery_method'])
    
    return df
    
