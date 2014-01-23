from collections import defaultdict

from lxml import etree
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient
import pandas
from sklearn import linear_model
from sklearn.externals import joblib

import sql_database
import helper

client = MongoClient()
db_mongo = client.yelp_database
posts = db_mongo.posts
rests_info = posts.find()

sql_db = sql_database.DbAccess('YELP', usr='root')

count = 0

socal_users = defaultdict(list)
norcal_users = defaultdict(list)

def get_restaurant(soup):
    links = soup.find_all('link')
    for link in links:
        href = link['href']
        if href.find('biz')!=-1:
            return href[href.find('biz')-1:]


def get_reviews(soup):
    lis = soup.find_all("li")
    reviews = [li for li in lis if li.get("class") and li.get("class")[0]=='review']
    return reviews

def build_row(user, norcal, socal):

    rest1 = socal[2]
    rest2 = norcal[2]
    price_diff = int(rest1[1]) - int(rest2[1])
    rating_diff = rest1[2] - rest2[2]
    meal_same = rest1[3]==rest2[3]
    table_same = rest1[4]==rest2[4]
    new_row = {'User': user, 'NorCalRest': norcal[0], 'NorCalRating': norcal[1], 'NorCalAvgRating': rest2[2], 'NorCalZip': rest2[7],
               'SoCalRest': socal[0], 'SoCalRating': socal[1], 'SoCalAvgRating': rest1[2], 'SoCalZip': rest1[7], 'r1Type': rest1[0],
               'r2Type': rest2[0], 'PriceDiff': price_diff, 'RatingDiff': rating_diff, 'MealSame': meal_same, 'TableSame': table_same, 'r1Food': rest1[5], 'r2Food': rest2[5]}
    return new_row

count = 0

for rest_info in rests_info:
    count += 1
    if count%100==0:
        print count

    if count>10000:
        break

    if 'yelp_page' not in rest_info:
        continue

    page = rest_info['yelp_page']
    soup = BeautifulSoup(page)

    restaurant = get_restaurant(soup)
    if not restaurant:
        continue

    nor_cal = False

    sql = ('''SELECT RestaurantType, RestaurantsPriceRange2, Rating, GoodForMeal, RestaurantsTableService, Favorites, Latitude, Zip
       FROM Restaurant WHERE Site = "''' + restaurant + '''" AND Rating IS NOT NULL;''')
    sql_db.cursor.execute(sql)
    sql_info = sql_db.cursor.fetchone()

    if not sql_info or any([obj=='NULL' for obj in sql_info]):
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

rows = []
for user in norcal_users:
    if user in socal_users:
        for norcal_rest in norcal_users[user]:
            for socal_rest in socal_users[user]:
                rows.append(build_row(user, norcal_rest, socal_rest))

f = open('data/commenters.txt', 'w')
f.write(str(rows))

df = pandas.DataFrame.from_records(rows)
df = helper.transform(df)
X = helper.BuildX(df)
logistic = joblib.load("data/logit.joblib.pkl")
df['scores'] = logistic.decision_function(X)
del df['r1Food']
del df['r1Type']
del df['r2Food']
del df['r2Type']
sql_db.cursor.execute('DROP TABLE IF EXISTS Review;')
pandas.io.sql.write_frame(df, 'Review', sql_db.cnx, flavor='mysql')

#Command = 'INSERT INTO Review (USERID, NorCalRest, NorCalRating, NorCalAvgRating, SoCalRest, SoCalRating, SoCalAvgRating) VALUES("%s", "%s", %f, %f, "%s", %f, %f);' % (user, norcal_rest[0], norcal_rest[1], norcal_rest[2], socal_rest[0], socal_rest[1], socal_rest[2])
#sql_db.cursor.execute(Command)
#sql_db.commit()
