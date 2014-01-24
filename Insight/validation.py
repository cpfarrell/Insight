#Third party modules
from pandas import DataFrame
import numpy as np
import pandas

#My modules
import sql_database
import predict_rest

db = sql_database.DbAccess('YELP', usr='root')

sql = ("SELECT DISTINCT SoCalRest FROM Review")
db.cursor.execute(sql)
SoCalRests = db.cursor.fetchall()

matches = []

for SoCalRest in SoCalRests:
    similar = predict_rest.predict_rest(SoCalRest[0], "10", "94117")
    sites = [rest['Site'] for rest in similar]
    for site in sites:
        sql = ('SELECT * FROM Review WHERE SoCalRest = "' + SoCalRest[0] + '" AND NorCalRest = "' + site + '";')
        db.cursor.execute(sql)
        CommonReviews = db.cursor.fetchall()
        if len(CommonReviews)>0:
            matches.append((SoCalRest[0], site))
            print SoCalRest[0] + ' ' + site + ' ' + str(len(CommonReviews))
print matches
