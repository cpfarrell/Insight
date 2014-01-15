#Third party modules
from flask import Flask, render_template, request
import numpy as np
from pandas import DataFrame
import pandas
from sklearn import linear_model
from sklearn.externals import joblib

import helper
import sql_database

db = sql_database.DbAccess('YELP', usr='root')
app = Flask(__name__)

@app.route("/")
def hello():
    print 'HELLO'
    return render_template('index.html')

@app.route("/restaurant")
def restaurant():
    #Get input arguments
    restaurant = request.args.get('restaurant', '')
    zip = request.args.get('zip', '')

    df = pandas.io.sql.read_frame('''
     SELECT r1.Site as r1Site, r1.RestaurantType as r1Type, r2.RestaurantType as r2Type, ABS(r1.RestaurantsPriceRange2 - r2.RestaurantsPriceRange2) as PriceDiff,
     ABS(r1.Rating - r2.Rating) as RatingDiff
     FROM Restaurant r1 JOIN ZipCodes
     ON (ZipCodes.Latitude - r1.Latitude)*(ZipCodes.Latitude - r1.Latitude)<0.0001 and 
     (ZipCodes.Longitude - r1.Longitude)*(ZipCodes.Longitude - r1.Longitude)<0.0001
     CROSS JOIN Restaurant r2
     WHERE r2.Site = "''' + restaurant + '''" AND ZipCodes.Zip = ''' + zip + ''';''', db.cnx)
     #WHERE r2.Site = '/biz/torta-sabrosa-south-san-francisco' AND ZipCodes.Zip = 94041;''', db.cnx)

    df = helper.transform(df)
    X = helper.BuildX(df)

    logistic = joblib.load("data/logit.joblib.pkl")
    scores = logistic.decision_function(X)
    return df.ix[int(np.argmax(scores)), 'r1Site']

@app.route('/<pagename>')
def regularpage(pagename=None):
    return "The page " + pagename + " does not exist"


if __name__ == "__main__":
    app.run()
