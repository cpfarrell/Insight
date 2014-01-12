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
#for rest_url in redis_db.get_members("restaurant_to_search"):
    rest_url = redis_db.random_member("restaurant_to_search")
    print rest_url
    rest = s.get("http://www.yelp.com" + rest_url)
#    rest = s.get('http://www.yelp.com/biz/kotoya-ramen-los-angeles-3')
    data_rest = rest.text
    redis_db.add_info(rest_url, {"yelp_page": data_rest})
    redis_db.add_to_group("restaurant_searched", rest_url)
    redis_db.remove_member("restaurant_to_search", rest_url)

    soup_rest = BeautifulSoup(data_rest)
    divs_rest = soup_rest.find_all('div')
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

    time.sleep(random.uniform(5,10))
