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

@app.route("/")
def hello():
    print 'HELLO'
    return render_template('index.html')

@app.route("/restaurant")
def restaurant():
    #Get input arguments
    restaurant = request.args.get('restaurant', '')
    miles = request.args.get('miles', '')
    zip = request.args.get('zip', '')
#    return restaurant + miles + zip
    return predict_rest.predict_rest(restaurant, miles, zip)

@app.route('/<pagename>')
def regularpage(pagename=None):
    return "The page " + pagename + " does not exist"


if __name__ == "__main__":
    app.run()
