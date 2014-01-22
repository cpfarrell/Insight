import json

#Third party modules
from flask import Flask, render_template, request
import numpy as np
from pandas import DataFrame
import pandas
from sklearn import linear_model
from sklearn.externals import joblib

import helper
import sql_database
import predict_rest

db = sql_database.DbAccess('YELP', usr='root')
app = Flask(__name__)
app.debug = True

similar = {}

@app.route("/")
def hello():
    return render_template('home.html')

@app.route("/maps")
def maps():
    restaurant = request.args.get('restaurant', '')
    miles = request.args.get('miles', '')
    zipcode = request.args.get('zipcode', '')
    return render_template('maps.html', restaurant=restaurant, miles=miles, zipcode=zipcode)

@app.route("/test2")
def testing():
    restaurant = request.args.get('restaurant', '')
    miles = request.args.get('miles', '')
    zipcode = request.args.get('zipcode', '')
    predict = predict_rest.predict_rest(restaurant, miles, zipcode)
    names = [rest[i][0] for i, rest in enumerate(predict)]
    items = [rest[i][1] for i, rest in enumerate(predict)]
    latitudes = [rest[i][2] for i, rest in enumerate(predict)]
    longitudes = [rest[i][3] for i, rest in enumerate(predict)]
    return render_template('maps.html', names=names, items=items, latitudes=latitudes, longitudes=longitudes)

@app.route("/restaurant")
def restaurant(new = False):
    #Get input arguments
    restaurant = request.args.get('restaurant', '')
    miles = request.args.get('miles', '')
    zipcode = request.args.get('zipcode', '')
    if (restaurant, miles, zipcode) not in similar:
        return json.dumps(predict_rest.predict_rest(restaurant, miles, zipcode))

def list_restaurants():
    q = request.args.get('q')
    # This is my query to find cities, countries matching query
    sql = ("SELECT FullName FROM Restaurant WHERE FullName LIKE '{0}%' LIMIT 10").format(q)
    db.cursor.execute(sql)
    # Matching cities are in a list
    restaurants = [restaurant[0] for restaurant in db.cursor.fetchall()]
    # Python list is converted to JSON string
    print restaurants
    return json.dumps(restaurants)

@app.route('/<pagename>')
def regularpage(pagename=None):
    return "The page " + pagename + " does not exist"

@app.route("/json/<what>")
def ajson(what):
    return list_restaurants()

if __name__ == "__main__":
    app.run()
