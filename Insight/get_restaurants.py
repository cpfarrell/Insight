from StringIO import StringIO
import time

from lxml import etree
from bs4 import BeautifulSoup
import requests

s = requests.Session()

for i in range(5):
    r = s.get('http://www.yelp.com/search?cflt=restaurants&find_loc=90025&start=' + str(10*i))
#r = s.get('http://www.yelp.com/biz/kotoya-ramen-los-angeles-3')
    data = r.text
    soup = BeautifulSoup(data)

    divs = soup.find_all('div')
    restaurants = [div.span.a['href'] for div in divs if div.get('class') and len(div.get('class'))>2 and div.get('class')[1] == 'natural-search-result']

    for restaurant in restaurants:
        print "http://www.yelp.com" + restaurant
        
    print '\n'
    time.sleep(5)

#divs[68].span.a['href']
