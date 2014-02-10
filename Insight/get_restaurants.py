from StringIO import StringIO
import time
import random

from lxml import etree
from bs4 import BeautifulSoup
import requests

import redis_database
import neighborhoods

s = requests.Session()

redis_db = redis_database.RedisDatabase()

pages_per_neighborhood = 500

for neighborhood in redis_db.get_members("neighborhoods"):
    if neighborhood not in neighborhoods.chicago:
        continue
    print neighborhood
    print redis_db.num_members(neighborhood)
    if redis_db.num_members(neighborhood) < 10*pages_per_neighborhood:
        print redis_db.num_members(neighborhood)
        start_page = redis_db.num_members(neighborhood)/10
        print start_page
        for i in range(start_page, pages_per_neighborhood):
            print i
            r = s.get('http://www.yelp.com/search?cflt=restaurants&find_loc=' + neighborhood + '&start=' + str(10*i))

            data = r.text
            soup = BeautifulSoup(data)
            divs = soup.find_all('div')
            restaurants = [div.span.a['href'] for div in divs if div.get('class') and len(div.get('class'))>2 and div.get('class')[1] == 'natural-search-result']

            if len(restaurants)==0:
                break

            for restaurant in restaurants:
                redis_db.add_to_group(neighborhood, restaurant)
                print "http://www.yelp.com" + restaurant
                if not redis_db.key_known(restaurant):
                    redis_db.add_key(restaurant)
                    redis_db.add_to_group("restaurant_to_search", restaurant)
                rest_info = redis_db.get_info(restaurant)
                all_neighborhoods = []
                if "neighborhoods" in rest_info:
                    all_neighborhoods = rest_info["neighborhoods"]
                all_neighborhoods.append(neighborhood)
                rest_info["neighborhoods"] = all_neighborhoods
                redis_db.add_info(restaurant, rest_info)
        
            time.sleep(random.uniform(20,30))

