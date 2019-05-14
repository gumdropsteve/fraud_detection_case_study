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