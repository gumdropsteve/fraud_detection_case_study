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
