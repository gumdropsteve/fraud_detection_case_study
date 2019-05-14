import warnings
import pandas as pd

# ignore warnings (bad practice)
warnings.filterwarnings('ignore')


def do_it(winstons_11_old=pd.read_json('data/data.json')):
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
