#Standard modules
from collections import defaultdict

#Third party modules
from pandas import DataFrame
import numpy as np
import pandas
from sklearn import linear_model
from sklearn.externals import joblib

#My modules
import helper
import sql_database
import predict_rest

db = sql_database.DbAccess('YELP', usr='root')

def validation(restaurant, miles, zipcode):
    df = pandas.io.sql.read_frame('''
     SELECT r1.Name as r1Name, r1.FullName as r1FullName, r1.RestaurantType as r1Type, 
     r2.RestaurantType as r2Type, ABS(r1.RestaurantsPriceRange2 - r2.RestaurantsPriceRange2) as PriceDiff,
     ABS(r1.Rating - r2.Rating) as RatingDiff, r1.Latitude as Latitude, r1.Longitude as Longitude, r1.GoodForMeal=r2.GoodForMeal as MealSame,
     r1.RestaurantsTableService=r2.RestaurantsTableService as TableSame, r1.Favorites as r1Food, r2.Favorites as r2Food '''
     #, r1.Review as r1Review, r2.Review as r2Review
     '''FROM Restaurant r1 JOIN ZipCodes
     ON DISTANCE(ZipCodes.Latitude, ZipCodes.Longitude, r1.Latitude, r1.Longitude) < ''' + miles + '''
     CROSS JOIN Restaurant r2
     WHERE r2.FullName = "''' + restaurant + '''" AND ZipCodes.Zip = ''' + zipcode + ''' AND r1.NReviews > 100 ORDER BY r1.FullName;''', db.cnx)

    df = helper.transform(df)

    #Use logistic regression to reduce list of possible restaurants
    X = helper.BuildX(df)
    logistic = joblib.load("data/logit.joblib.pkl")
    df['scores'] = logistic.decision_function(X)
    df = df.sort('scores', ascending=False).reset_index()
    #df = df.ix[range(30),:]
    df =df.ix[df['scores']>3]
    #Sort by name to keep aligned
    df = df.sort('r1FullName')

    #Grab reviews from those restaurants. Python sort instead of SQL ORDER BY because of different treatment of capitalized letters
    r1FullNames = '", "'.join(df['r1FullName'].tolist())
    db.cursor.execute('SELECT FullName, Review FROM Restaurant WHERE FullName IN ("' + r1FullNames + '") AND NReviews > 100 ORDER BY FullName;')
    r1Reviews = db.cursor.fetchall()
    r1Reviews = sorted(r1Reviews)

    db.cursor.execute('SELECT FullName, Review FROM Restaurant WHERE FullName = "' + restaurant + '";')
    r2Review = db.cursor.fetchone()

    df = tf_idf(df, r1Reviews, r2Review)
    restaurants = []
    for i in range(n_restaurants):
        print df.ix[i, 'max_words']
        restaurants.append({i :(df.ix[i, 'r1Name'], (df.ix[i, 'max_words']), df.ix[i, 'Latitude'], df.ix[i, 'Longitude'])})

    print restaurants

if __name__=='__main__':
#    predict_rest("Kotoya Ramen 11901 Santa Monica Blvd Los Angeles, CA 90025", "10", "94117")
    predict_rest("Juquila Restaurant 11619 Santa Monica Blvd Los Angeles, CA 90025", "15", "94117")
