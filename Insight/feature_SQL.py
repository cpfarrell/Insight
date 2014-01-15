#Extracts features from yelp html page and inserts them into SQL database
#Lots of restaurants are skipped if yelp page doesn't have full information

from lxml import etree
from bs4 import BeautifulSoup

import redis_database
import sql_database

redis_db = redis_database.RedisDatabase()

attrs = ['Alcohol', 'HasTV', 'NoiseLevel', 'RestaurantsAttire', 'BusinessAcceptsCreditCards', 'Ambience', 'RestaurantsGoodForGroups', 'Caters', 'WiFi', 'RestaurantsReservations', 'RestaurantsTakeOut', 'GoodForKids', 'WheelchairAccessible', 'RestaurantsTableService', 'OutdoorSeating', 'RestaurantsPriceRange2', 'RestaurantsDelivery', 'GoodForMeal', 'BusinessParking']

db = sql_database.DbAccess('YELP', usr='root')
db.cursor.execute('DROP TABLE IF EXISTS Restaurant;')

Columns = 'Site CHAR(100), Rating FLOAT, Favorites CHAR(200), RestaurantType CHAR(200), Latitude FLOAT, Longitude FLOAT, SimilarRest1 CHAR(100)'
Columns += ', SimilarRest2 CHAR(100), SimilarRest3 CHAR(100)'

for attr in attrs:
    Columns += ', ' + attr + ' CHAR(80)'

db.cursor.execute('CREATE TABLE Restaurant (' + Columns + ');')

count = 0
for restaurant in redis_db.get_members("restaurant_searched"):
    count += 1
    if count%100==0:
        db.commit()

    rest_info = redis_db.get_info(restaurant)
    page = rest_info['yelp_page']
    soup = BeautifulSoup(page)
    divs = soup.find_all('div')

    new_info = {}

    bizRating = [div for div in divs if div.get("id")=="bizRating"]

    #Fails if page essentially has no info
    if len(bizRating)==0:
        continue
    new_info["Rating"] = bizRating[0].meta['content']

    #Get ngrams from snippets
    review_snippets = [div for div in divs if div.get("class") and len(div.get("class"))>1 and div.get("class")[0]=="media-story" and div.get("class")[1]=="snippet"]
    ngrams = []
    for snippet in review_snippets:
        for object in snippet.contents:
            try:
                if object.get('ngram'):
                    ngrams.append(object.get('ngram'))
            except:
                continue
    new_info["Ngrams"] = ngrams

    #Grab all the header data on the restaurant page
    dds = soup.find_all('dd')
    for dd in dds:
        content = dd.contents[0]
        #Convert price to a scale from 1 to 4
        if dd['class'][0].find("RestaurantsPriceRange2")!=-1:
            content = 4 - len(dd.span.span['data-remainder'])
        new_info[str(dd['class'][0])[5:]] = str(content)

    #Get the type of the restaurant
    bizInfo = [div for div in divs if div.get("id")=="bizInfoContent"]
    spans = bizInfo[0].find_all('span')
    category = [span for span in spans if span.get('id')=="cat_display"][0]
    restaurant_type = [content.contents[0].lstrip() for content in category.contents if hasattr(content, 'contents')]
    new_info['restaurant_type'] = restaurant_type

    #Get similar restaurants
    rec_bizs = [div for div in divs if div.get("id")=="bizSimilarBox"]
    if len(rec_bizs)==0:
        continue
    rec_links = [rec_biz['href'] for rec_biz in rec_bizs[0].find_all('a') if str(rec_biz.get("id")).find("bizreclink")!=-1]
    if len(rec_links)<3:
        continue


    #Get latitude and longitude from map
    imgs = soup.find_all('img')
    if len([img['src'] for img in imgs if img.get("alt")=="Map of Business"])==0:
        continue
    map = [img['src'] for img in imgs if img.get("alt")=="Map of Business"][0]
    lat = map[map.find('center')+7:map.find("%2C")]
    long = map[map.find('%2C')+3:map.find("&language")]


    #Now insert all this information into SQL
    Values = 'INSERT INTO Restaurant (Site, Rating, Favorites, RestaurantType, Latitude, Longitude, SimilarRest1, SimilarRest2, SimilarRest3'
    for attr in attrs:
        Values += ', ' + attr
        
    Values += ') VALUES ("' + restaurant + '", ' + bizRating[0].meta["content"] + ', "' + "---".join(ngrams) + '", "' + "---".join(restaurant_type) + '", '
    Values += lat + ', ' +  long + ', "' + rec_links[0] + '", "' + rec_links[1] + '", "' + rec_links[2]

    for attr in attrs:
        if attr not in new_info:
            new_info[attr] = "NULL";
        Values += '", "' + new_info[attr]

    Values += '");'

    for attr in attrs:
        Columns += ', ' + attr + ' CHAR(80)'

    Values += ';'
    db.cursor.execute(Values)

db.commit()
db.close()
