import json
import ast

#Third party modules
from flask import Flask, render_template, request
import numpy as np
from pandas import DataFrame
import pandas
from sklearn import linear_model
from sklearn.externals import joblib
from pygeocoder import Geocoder

import helper
import sql_database
import predict_rest

db = sql_database.DbAccess('INSIGHT', usr='root')
app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
    return render_template('home.html')

@app.route("/maps")
def maps():
    restaurant = request.args.get("restaurant", "")
    miles = request.args.get("miles", "")
    zipcode = request.args.get("zipcode", "")
    return render_template('maps.html', restaurant=restaurant, miles=miles, zipcode=zipcode)

@app.route("/restaurant")
def restaurant():
    #Get input arguments
    restaurant = request.args.get("restaurant", "")
    miles = request.args.get("miles", '')
    zipcode = request.args.get("zipcode", "")
    try:
        miles = str(int(float(miles)))
        if miles=="0":
            miles = "1"
    except ValueError:
        return json.dumps(["Please enter a number into the miles field"])

    try:
        location = Geocoder.geocode(zipcode)
    except:
        return json.dumps(["I couldn't recognize that address. Could you enter another one?"])

    zipcode = location.formatted_address

    query = restaurant + " " + miles + " " + zipcode
    sql = ('SELECT Result FROM Cached WHERE Query = "' + query + '";')
    db.cursor.execute(sql)
    results = db.cursor.fetchall()
    if len(results)>0:
        result = ast.literal_eval(results[0][0])
    else:
        result = predict_rest.predict_rest(restaurant, miles, location)
        sql = ('INSERT INTO Cached (Query, Result) VALUES ("' + query + '", %s);')
        db.cursor.execute(sql, (str(result),))
        db.commit()

    return json.dumps(result)

def list_restaurants():
    q = request.args.get('q')
    # This is my query to find cities, countries matching query
    sql = ('SELECT FullName FROM Restaurant WHERE FullName LIKE "{0}%" LIMIT 10').format(q)
    db.cursor.execute(sql)
    # Matching cities are in a list
    restaurants = [restaurant[0] for restaurant in db.cursor.fetchall()]
    # Python list is converted to JSON string
    return json.dumps(restaurants)

funcs = {
        "restaurants": list_restaurants
}

@app.route("/json/<what>")
def ajson(what):
    if what=='restaurants':
        return funcs[what]()
    else:
        return json.dumps([])

@app.route('/<pagename>')
def regularpage(pagename=None):
    return "The page " + pagename + " does not exist"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
#    app.run()
