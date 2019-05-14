def correlation_matrix():
    import pandas as pd
    import warnings
    # ignore warnings (bad practice)
    warnings.filterwarnings('ignore')

    def new_df():
        def avg_price(tic_lst):
            res = 0
            numer = 0
            denom = .001
            for tic in tic_lst:
                # get our total quantity of tickets
                denom += tic['quantity_total']
                numer += tic['cost'] * tic['quantity_total']

            res = numer / denom
            return res

        def a_convert(df_old):
            '''
            inputs: a Dataframe of ticket information
            returns: dataframe with venue_name and venue_address as booleans, 
            indicating whether or not that info is present.
            drops other venue-based columns due to multi-colinearity
            also replaces ticket_types with avg_prices
            '''
            # venue transformation
            df = df_old.copy()
            # get our average price, derived from ticket_types
            df['avg_price'] = df['ticket_types'].apply(avg_price)
            df['venue_name'] = (df['venue_name'].apply(lambda x: False if not x else len(x)>0).astype(int))
            df['venue_address'] = (df['venue_address'].apply(lambda x: False if not x else len(x)>0).astype(int))
            df = df.drop(['ticket_types','venue_country','venue_state','venue_latitude','venue_longitude'], axis=1)
            return df

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
            df['fraud'] = df['acct_type'].apply(lambda x: x[:5] == 'fraud').astype(int)
            #drop unused columns
            dropped_cols = ['name', 'acct_type','approx_payout_date','channels','country','currency','description', 'email_domain']
            df.drop(dropped_cols, inplace = True, axis = 1)
            #create event_delay
            df['event_delay'] = df['event_end'] - df['event_created']
            #One-hot encode 'delivery'
            df = pd.get_dummies(df, prefix = 'delivery', columns = ['delivery_method'])
            return df


        def do_it(winstons_11_old):
            '''
            returns edited columns from the 11 columns assigned to winston
            '''
            winstons_11 = winstons_11_old.copy()
            '''event_published'''  # events not published are 11.275153537038442x more likely to be fraudulent
            # set events null values for event_published to 0 and those with values as 1 in new column
            winstons_11[ 'event_published' ] = ( ~winstons_11[ 'event_published' ].isnull() ).astype(int)
            '''has_header'''  # events without header are 2.237528153797371x more likely to be fraudulent  
            # set events null values for has_header to 0 and those with values as 1 in new column
            winstons_11[ 'has_header' ] = ( ~winstons_11[ 'has_header' ].isnull() ).astype(int)
            '''event_start'''  # epoch time -- nothing of interest at this time 
            '''fb_published'''  # include , good to go 
            '''gts'''  # check zero_gts values and gts 
            # max , min  # (306293.93, 0.0)
            # median , mean  # (431.93, 2430.2314919439214)
            # add zero column
            winstons_11[ 'zero_gts' ] = (winstons_11[ 'gts' ] > 0).astype(int)
            '''has_analytics'''  # include , good to go 
            '''has_logo'''  # include , good to go 
            '''listed'''  # values: y , n ; convert to 1 , 0
            # convert to bool value (y=1 , n=0)
            winstons_11[ 'listed' ] = (winstons_11[ 'listed' ] == 'y').astype(int)
            '''name'''  # ignore for now 
            '''name_length'''  # ignore for now 
            '''num_order'''  # ranging values ; add zero_num_order (357 values == 0)
            # max , min  # (2000, 0)
            # median , mean  # (8.0, 28.01067168863779)
            # add zero column
            winstons_11[ 'zero_num_order' ] = (winstons_11[ 'num_order' ] > 0).astype(int)
            return winstons_11

        return max_data_pipeline(jconvert(a_convert(do_it(pd.read_json('data/data.json')))))

    def corr_matrix(df):
        # with pandas / numpy
        corr = df.corr()
        corre_matrix = corr.style.background_gradient( cmap='coolwarm' )
        # 'RdBu_r' & 'BrBG' are other good diverging colormaps
        return corre_matrix
    
    return corr_matrix(new_df())