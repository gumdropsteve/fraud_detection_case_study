import os
from requests import get
from bs4 import BeautifulSoup
from contextlib import closing
from requests.exceptions import RequestException

site = 'http://galvanize-case-study-on-fraud.herokuapp.com/data_point'

def l(e):  # prints errors  # need to make this post to permanent log
    print(e)


def good_respons(e):  # Returns True if the response seems to be HTML, False otherwise.
    content_type = e.headers['Content-Type'].lower()
    return (e.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def pull_content(dom):  # Attempts to get the content at `url` (dom) by making an HTTP GET request.
    try:
        with closing(get(dom, stream=True)) as e:
            if good_respons(e):  # If the content-type of response is some kind of HTML/XML
                print('sdf')
                return e.content  # return the text content
            else:
                return f'bad response {e}'
    except RequestException as e:  # otherwise return None
        raise Exception(f'Error during requests to {dom} : {e}')


def bring_the_info(base_url):
    response = pull_content(base_url)
    if response is not None:  # url accessibility check
        html = BeautifulSoup(response, 'html.parser')
        many_datas = set()
        for ul in html.select('//*[@id="content"]'):  
            for info in ul.text.split('\n'):
                if len(info) > 0:
                    many_datas.add(info.strip())
        the_info = list(many_datas)
        return the_info
    # Raise an exception if we failed to get any data from the url
    raise Exception(f'Error retrieving the_info at {base_url}')
    # use of 'raise' eliminates need for 'else' following 'if'  # seems to be in a replacing fashion


print(pull_content(site))


# def comps(existing_results, city_short_link):
#     '''
#     input) previously seen listngs {existing_results} for city of interest
#     input) link to city of interest listings sorted by newness {city_short_link}

#     1) pulls most recent new listings from city_short_link (usualy 12, range 10-13)
#         based on results of searching that city, gridview, sorting for newest results
#     2) compares the addresses of those listings to the previously seen listings (log) for that city

#     output) new listings in that city 
#         which are in the first page of new listings 
#         and are not existing_results (log) for that city 
#     '''
#     results = []  # short term log for first encounter listings
#     in_existing_results_count: int = 0  # specified int, not sure if any different from just x = 0, doubt it is
#     for listing in pull_the_new_pleasanton_listings(city_short_link):  # for data in datas
#         if listing not in results:  # if not a double post
#             if listing not in existing_results:  # if an unseen listing
#                 results.append(listing)  # add listing to results
#             elif listing in existing_results:  # if previously logged
#                 in_existing_results_count += 1  # add 1 to in_existing_results_count
#         elif listing in results:  # instance unseen
#             print('existing in results (possible double listing?)', listing)  # error unseen (hedge)
#         else:
#             print('we got to else.. f.')
#     if len(results) > 1:  # if multiple new listings
#         multi_result_dict = []
#         for result in results:
#             multi_result_dict.append(result)
#         return multi_result_dict
#     elif len(results) == 1:  # expected most common actionable response once in routine
#         return results  # broken down asap
#     elif len(results) == 0:  # expected most common response once in routine
#         raise Exception(f'No New Listings in Pleasanton {city_short_link}')
#     else:
#         raise Exception('F')
