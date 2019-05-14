"""

"""
import pandas as pd
from IPython.display import HTML, display
import seaborn as sns
import matplotlib.pyplot as plt

def jconvert(df_old):
    """
    take the fraud dataframe, and edit columns 22-33
    input: dataframe
    output: dataframe with all numbers

    For now:
    ['num_payouts', 'object_id', 'org_desc', 'org_facebook', 'org_name',
       'org_twitter', 'payee_name', 'payout_type', 'previous_payouts',
       'sale_duration', 'sale_duration2']

       changes to
      ['num_payouts', 'org_desc', 'org_facebook', 'org_name',
       'org_twitter', 'payee_name', 'pay_by_check', 'has_payout_type',
       'sale_duration'],

        check if the org has a facebook, twitter, name, description, name of payee
        Change the respective columns to 1 or 0
        drop previous_payouts, since it'll be complicated and may not give more info
        drop sale_duration2 for collinearity with sale_duration
        Also add a fraud column as target
        drop object_id. probably not important?
    """
    df = df_old.copy()
    df['sale_duration'] = df['sale_duration'].fillna(0)
    df['org_name'] = df['org_name'].apply(lambda x: len(x) > 0).astype(int)
    df['org_desc'] = df['org_desc'].apply(lambda x: len(x) > 0).astype(int)
    df['payee_name'] = df['payee_name'].apply(lambda x: len(x) > 0).astype(int)
    df['pay_by_check'] = (df['payout_type'] == 'CHECK').astype(int)
    df['has_payout_type'] = (df['payout_type'] != '').astype(int)
    df['org_facebook'] = (df['org_facebook'] > 0).astype(int)
    df['org_twitter'] = (df['org_twitter'] > 0).astype(int)
    df = df.drop(['object_id', 'sale_duration2', 'previous_payouts', 'payout_type'], axis = 1)
    return df

if __name__== '__main__':
    """
    random testing code. just ignore
    """
    df = pd.read_json('data/data.json')

    df['fraud'] = df['acct_type'].apply(lambda x: x[:5]) == 'fraud'

    my_columns = df.columns[22:33]
    df_mine = df[list(my_columns) + ['fraud']]

    #sns.pairplot(df_mine, hue = 'fraud')
    #plt.show()

    df_bad = df_mine[df_mine['fraud']]
    df_good = df_mine[~df_mine['fraud']]

    df_mine['org_has_name'] = df_mine['org_name'].apply(lambda x: len(x) > 0)
    df_mine['org_has_desc'] = df_mine['org_desc'].apply(lambda x: len(x) > 0)

    y = df_mine['fraud']

"""
num_payouts         : fraud has it extremely low
object_id           : fraud seems more spread out?
org_desc            : run nlp on this maybe? also, empty names are more common in fraud
org_facebook        : not sure of meaning - fraud had a higher proportion of zeroes tho. max is similar.
org_name            : nlp? also, fraud has more empty names
org_twitter         : Like facebook
payee_name          : probably check existence
payout_type         : non fraud -> higher proportion of check. almost nonexistent in fraud
previous_payouts    : can convert into something like num_payouts? also maybe something like total amount
sale_duration       : more missing in fraud? negative values - user error, or "presale"
sale_duration2      : like sale duration 1. Both are lower in fraud
"""
