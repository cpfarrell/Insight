from StringIO import StringIO
import time
import random

from lxml import etree
from bs4 import BeautifulSoup
import requests
import pymongo
from pymongo import MongoClient

import redis_database

redis_db = redis_database.RedisDatabase()
client = MongoClient()
db = client.yelp_database
posts = db.posts

s = requests.Session()

while redis_db.num_members("restaurant_to_search") > 0:
    rest_url = redis_db.random_member("restaurant_to_search")
    print rest_url
    rest = s.get("http://www.yelp.com" + rest_url)

    rest_info = {'restaurant': rest_url}
    data_rest = rest.text
    rest_info['yelp_page'] = data_rest

    soup_rest = BeautifulSoup(data_rest)
    divs_rest = soup_rest.find_all('div')

    pages_rest = [div for div in divs_rest if div.get("id") and div.get("id")=="rpp-count"]
    n_reviews = 0
    if len(pages_rest)>0:
        try:
            n_reviews = int(pages_rest[0].contents[0].split()[-1])
        except:
            n_reviews = int(pages_rest[0].contents[0].split()[-2])

    rest_info['reviews'] = n_reviews
    print n_reviews
    #Loop through and grab up to four more pages of reviews
    pages = n_reviews/40
    for i in range(1,pages+1):
        if i > 4:
            break
        rest = s.get("http://www.yelp.com" + rest_url + "?start=" + str(40*i))
        data_rest = rest.text
        rest_info['yelp_page' + str(i)] = data_rest
        time.sleep(random.uniform(2,6))

    #Grab the menu if possible as well
    menu_url_list = [div for div in divs_rest if div.get('class') and div['class']==["yelp-menu"]]
    if menu_url_list:
        menu_url = menu_url_list[0].a['href']

        time.sleep(random.uniform(5,15))
        menu = s.get('http://www.yelp.com' + menu_url)
        data_menu = menu.text
        rest_info['yelp_menu'] = data_menu


    posts.insert(rest_info)
    print rest_info.keys()
    redis_db.add_to_group("restaurant_with_info", rest_url)
    redis_db.remove_member("restaurant_to_search", rest_url)
    time.sleep(random.uniform(2,6))
