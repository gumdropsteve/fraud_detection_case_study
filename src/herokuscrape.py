import csv
import requests
import pandas as pd
from time import sleep
from urllib.request import urlopen


def heroku_scrape( n_loops , pause ):
    """
    input: number of loops {n_loops}
        note: if > 9000 , n_loops = ∞
    input: how long to sleep between loops {pause}
    
    make a function that scrapes the website, 
    checks if the scraped dictionary is the same as the previous one.
    add to csv
    """
    # inital scrape
    def scrape_data():
        # set target 
        r = requests.get( 'http://galvanize-case-study-on-fraud.herokuapp.com/data_point' )
        # extract data
        event_dict = r.json()
        # set standard 
        new_data = pd.DataFrame( [event_dict] )
        # open and add to csv
        with open( 'data/test_script_examples.csv' , 'a' ) as f:
            new_data.to_csv( f , header=False )
        sleep( int(pause) )  

    # loop-de-loop
    def scrape_forever():
        print( 'oof' )
        i = 1
        _ = 0
        while i > 0:
            scrape_data()
            print(_)
            _ += 1

    if n_loops > 9000.0:
        scrape_forever()
    else:
        for _ in range( n_loops ):
            scrape_data()
            print( n_loops - _ )


print(heroku_scrape( 9000.1 , 30 ))
