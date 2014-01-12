from StringIO import StringIO
import time
import random

from lxml import etree
from bs4 import BeautifulSoup
import requests

import redis_database

s = requests.Session()

redis_db = redis_database.RedisDatabase()

pages_per_neighborhood = 20

for neighborhood in redis_db.get_members("neighborhoods"):
    print neighborhood
    print redis_db.num_members(neighborhood)
    if redis_db.num_members(neighborhood) < 10*pages_per_neighborhood:
        for i in range(pages_per_neighborhood):
            r = s.get('http://www.yelp.com/search?cflt=restaurants&find_loc=' + neighborhood + '&start=' + str(10*i))

            data = r.text
            soup = BeautifulSoup(data)
            divs = soup.find_all('div')
            restaurants = [div.span.a['href'] for div in divs if div.get('class') and len(div.get('class'))>2 and div.get('class')[1] == 'natural-search-result']

            for restaurant in restaurants:
                redis_db.add_to_group(neighborhood, restaurant)
                print "http://www.yelp.com" + restaurant
                if not redis_db.key_known(restaurant):
                    redis_db.add_key(restaurant)
                    redis_db.add_to_group("restaurant_to_search", restaurant)
        
            time.sleep(random.uniform(15,20))

