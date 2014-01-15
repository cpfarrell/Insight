from StringIO import StringIO
import time
import random

from lxml import etree
from bs4 import BeautifulSoup
import requests

import redis_database

redis_db = redis_database.RedisDatabase()

s = requests.Session()

while redis_db.num_members("restaurant_to_search") > 0:
    rest_url = redis_db.random_member("restaurant_to_search")
    print rest_url
    rest = s.get("http://www.yelp.com" + rest_url)

    data_rest = rest.text
    redis_db.add_info(rest_url, {"yelp_page": data_rest})
    redis_db.add_to_group("restaurant_searched", rest_url)
    redis_db.remove_member("restaurant_to_search", rest_url)

    soup_rest = BeautifulSoup(data_rest)
    divs_rest = soup_rest.find_all('div')

    pages_rest = [div for div in divs_rest if div.get("id") and div.get("id")=="rpp-count"]
    n_reviews = 0
    if len(pages)>0:
        try:
            n_reviews = int(pages[0].contents[0].split()[-1])
        except:
            n_reviews = int(pages[0].contents[0].split()[-2])
    redis_db.add_info(restaurant, {"reviews": n_reviews}) 

    #Grab all the reviews from subsequent pages
    pages = n_reviews/40
    for i in range(1,pages+1):
        rest = s.get("http://www.yelp.com" + rest_url + "?start=" + str(40*i))
        data_rest = rest.text
        redis_db.add_info(rest_url, {"yelp_page" + str(i): data_rest})
        redis_db.add_to_group("restaurant_full_reviews", rest_url)
        time.sleep(random.uniform(15,20))

    menu_url_list = [div for div in divs_rest if div.get('class') and div['class']==["yelp-menu"]]
    if menu_url_list:
        menu_url = menu_url_list[0].a['href']

        time.sleep(random.uniform(5,10))
        menu = s.get('http://www.yelp.com' + menu_url)
        data_menu = menu.text
        redis_db.add_info(rest_url,{"yelp_menu": data_menu})
        soup_menu = BeautifulSoup(data_menu)
        print len(str(soup_menu))

    else:
        print 'No menu found'

    time.sleep(random.uniform(10,15))
