#Standard modules
import json

#Third party modules
from pandas import DataFrame
import numpy as np
import pandas
from sklearn import linear_model
from sklearn.externals import joblib

#My modules
import helper
import sql_database
db = sql_database.DbAccess('YELP', usr='root')

def predict_rest(restaurant, miles, zip):
    df = pandas.io.sql.read_frame('''
     SELECT r1.Name as r1Name, r1.RestaurantType as r1Type, r2.RestaurantType as r2Type, ABS(r1.RestaurantsPriceRange2 - r2.RestaurantsPriceRange2) as PriceDiff,
     ABS(r1.Rating - r2.Rating) as RatingDiff, r1.Latitude as Latitude, r1.Longitude as Longitude
     FROM Restaurant r1 JOIN ZipCodes
     ON DISTANCE(ZipCodes.Latitude, ZipCodes.Longitude, r1.Latitude, r1.Longitude) < ''' + miles + '''
     CROSS JOIN Restaurant r2
     WHERE r2.Name = "''' + restaurant + '''" AND ZipCodes.Zip = ''' + zip + ''';''', db.cnx)

    df = helper.transform(df)
    X = helper.BuildX(df)

    logistic = joblib.load("data/logit.joblib.pkl")
    df['scores'] = logistic.decision_function(X)
    df = df.sort('scores', ascending=False).reset_index()

    address = []
    names = ""
    for i in range(3):
        names += str(i+1) + '. ' + df.ix[i, 'r1Name'] + '<br>'
        address.append({i :(df.ix[i, 'r1Name'], df.ix[i, 'Latitude'], df.ix[i, 'Longitude'])})
    #restaurants = {'names': names, 'address': address}

    #print restaurants
    #return json.dumps(restaurants)
    return json.dumps(address)

if __name__=='__main__':
    predict_rest("Brennan's Restaurant", "10", "94114")
