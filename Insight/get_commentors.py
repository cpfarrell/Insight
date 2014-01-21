from collections import defaultdict

from lxml import etree
from bs4 import BeautifulSoup

import redis_database
import sql_database

redis_db = redis_database.RedisDatabase()
db = sql_database.DbAccess('YELP', usr='root')
db.cursor.execute('DROP TABLE IF EXISTS Review;')
db.cursor.execute('''CREATE TABLE Review (USERID CHAR(80), NorCalRest CHAR(150), NorCalRating FLOAT, NorCalAvgRating FLOAT, 
                  SoCalRest CHAR(150), SoCalRating FLOAT, SoCalAvgRating FLOAT);''')

count = 0

socal_users = defaultdict(list)
norcal_users = defaultdict(list)

def get_reviews(soup):
    lis = soup.find_all("li")
    reviews = [li for li in lis if li.get("class") and li.get("class")[0]=='review']
    return reviews

count = 0
for restaurant in redis_db.get_members("restaurant_searched"):
    count += 1
    if count%100==0:
        print count

    if count>30:
        break

    rest_info = redis_db.get_info(restaurant)
    nor_cal = False
    print restaurant

    sql = ('''SELECT RestaurantType, RestaurantsPriceRange2, Rating, GoodForMeal, RestaurantsTableService, Favorites, Latitude
       FROM Restaurant WHERE Site = "''' + restaurant + '''";''')
    db.cursor.execute(sql)
    sql_info = db.cursor.fetchone()
    if not sql_info:
        continue

    if sql_info[6] > 36.1075:
        nor_cal = True

    reviews = []
    for i in range(5):
        idx = ''
        if i != 0:
            idx = str(i)

        if ('yelp_page' + idx) in rest_info:
            page = rest_info['yelp_page' + idx]
            soup = BeautifulSoup(page)

            if i == 0:
                imgs = soup.find_all('img')
                if len([img['src'] for img in imgs if img.get("alt")=="Map of Business"])==0:
                    break
                map = [img['src'] for img in imgs if img.get("alt")=="Map of Business"][0]
                lat = float(map[map.find('center')+7:map.find("%2C")])

                if lat > 36.1075:
                    nor_cal = True

                divs = soup.find_all('div')
                bizRating = [div for div in divs if div.get("id")=="bizRating"]
                if len(bizRating)==0:
                    continue
                avg_rating = float(bizRating[0].meta['content'])

            reviews.extend(get_reviews(soup))

    for review in reviews:
        userid_url = review.a['href']
        userid = userid_url[userid_url.find("userid")+7:]
        rating = float(review.meta['content'])

        if nor_cal:
            norcal_users[userid].append((restaurant, rating, sql_info))
        else:
            socal_users[userid].append((restaurant, rating, sql_info))

for user in norcal_users:
    if user in socal_users:
        for norcal_rest in norcal_users[user]:
            for socal_rest in socal_users[user]:
                print user
#                Command = 'INSERT INTO Review (USERID, NorCalRest, NorCalRating, NorCalAvgRating, SoCalRest, SoCalRating, SoCalAvgRating) VALUES("%s", "%s", %f, %f, "%s", %f, %f);' % (user, norcal_rest[0], norcal_rest[1], norcal_rest[2], socal_rest[0], socal_rest[1], socal_rest[2])
#                db.cursor.execute(Command)
#                db.commit()
