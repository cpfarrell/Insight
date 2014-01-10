from StringIO import StringIO
import time
import random

from lxml import etree
from bs4 import BeautifulSoup
import requests

s = requests.Session()

rest_urls = [
'http://www.yelp.com/biz/sunny-blue-santa-monica',
'http://www.yelp.com/biz/tar-and-roses-santa-monica',
'http://www.yelp.com/biz/bay-cities-italian-deli-and-bakery-santa-monica',
'http://www.yelp.com/biz/melisse-santa-monica-2',
'http://www.yelp.com/biz/the-misfit-restaurant-bar-santa-monica',
'http://www.yelp.com/biz/fritto-misto-santa-monica',
'http://www.yelp.com/biz/urth-caffe-santa-monica',
'http://www.yelp.com/biz/musha-restaurant-santa-monica',
'http://www.yelp.com/biz/manchego-santa-monica',
'http://www.yelp.com/biz/blue-stove-santa-monica',
'http://www.yelp.com/biz/true-food-kitchen-santa-monica',
'http://www.yelp.com/biz/seasalt-fish-grill-santa-monica',
'http://www.yelp.com/biz/fathers-office-santa-monica',
'http://www.yelp.com/biz/upper-west-santa-monica',
'http://www.yelp.com/biz/umami-burger-santa-monica',
'http://www.yelp.com/biz/cha-cha-chicken-santa-monica',
'http://www.yelp.com/biz/mercado-santa-monica',
'http://www.yelp.com/biz/the-lobster-santa-monica',
'http://www.yelp.com/biz/superfood-express-santa-monica',
'http://www.yelp.com/biz/peas-and-carrots-santa-monica',
'http://www.yelp.com/biz/spazio-caff%C3%A9-santa-monica',
'http://www.yelp.com/biz/santa-monica-seafood-santa-monica',
'http://www.yelp.com/biz/milo-and-olive-santa-monica',
'http://www.yelp.com/biz/la-vecchia-cucina-santa-monica',
'http://www.yelp.com/biz/warszawa-santa-monica',
'http://www.yelp.com/biz/the-counter-santa-monica',
'http://www.yelp.com/biz/rustic-canyon-santa-monica',
'http://www.yelp.com/biz/library-alehouse-santa-monica',
'http://www.yelp.com/biz/ushuaia-argentinean-steakhouse-santa-monica',
'http://www.yelp.com/biz/boa-steakhouse-santa-monica',
'http://www.yelp.com/biz/stella-barra-pizzeria-santa-monica',
'http://www.yelp.com/biz/eat-shabu-santa-monica-2',
'http://www.yelp.com/biz/tacos-punta-cabras-santa-monica',
'http://www.yelp.com/biz/hillstone-restaurant-santa-monica',
'http://www.yelp.com/biz/tender-greens-santa-monica',
'http://www.yelp.com/biz/california-chicken-cafe-santa-monica',
'http://www.yelp.com/biz/brus-wiffle-a-waffle-joint-santa-monica',
'http://www.yelp.com/biz/il-ristorante-di-giorgio-baldi-santa-monica',
'http://www.yelp.com/biz/jiraffe-santa-monica',
'http://www.yelp.com/biz/joes-pizza-santa-monica',
'http://www.yelp.com/biz/z-garden-santa-monica',
'http://www.yelp.com/biz/r-d-kitchen-santa-monica',
'http://www.yelp.com/biz/pono-burger-santa-monica',
'http://www.yelp.com/biz/shaka-shack-burgers-santa-monica',
'http://www.yelp.com/biz/lares-restaurant-santa-monica',
'http://www.yelp.com/biz/thyme-cafe-and-market-santa-monica',
'http://www.yelp.com/biz/kafe-k-santa-monica',
'http://www.yelp.com/biz/capo-santa-monica',
'http://www.yelp.com/biz/tacos-por-favor-santa-monica',
'http://www.yelp.com/biz/huckleberry-santa-monica']

for rest_url in rest_urls:
    print rest_url
    rest = s.get(rest_url)
#    rest = s.get('http://www.yelp.com/biz/kotoya-ramen-los-angeles-3')
    data_rest = rest.text
    soup_rest = BeautifulSoup(data_rest)

    divs_rest = soup_rest.find_all('div')
    menu_url_list = [div for div in divs_rest if div.get('class') and div['class']==["yelp-menu"]]
    if menu_url_list:
        menu_url = menu_url_list[0].a['href']

        time.sleep(random.uniform(2,7))
        menu = s.get('http://www.yelp.com' + menu_url)
        data_menu = menu.text
        soup_menu = BeautifulSoup(data_menu)
        print len(str(soup_menu))
        time.sleep(random.uniform(2,7))

    else:
        print 'No menu found'
