from pandas import DataFrame
import numpy as np
import pandas
from sklearn import linear_model
from sklearn.externals import joblib
from sklearn import cross_validation

import helper
import sql_database
db = sql_database.DbAccess('YELP', usr='root')

def main():
    df_match = pandas.io.sql.read_frame('''
       SELECT r1.RestaurantType as r1Type, r2.RestaurantType as r2Type, ABS(r1.RestaurantsPriceRange2 - r2.RestaurantsPriceRange2) as PriceDiff,
       ABS(r1.Rating - r2.Rating) as RatingDiff
       FROM Restaurant r1 JOIN Restaurant r2 ON r1.Site = r2.SimilarRest1 or r1.Site = r2.SimilarRest2 or r1.Site = r2.SimilarRest3;''',db.cnx)
    df_match['Match'] = np.ones(len(df_match))

    df_nomatch = pandas.io.sql.read_frame('''
       SELECT r1.RestaurantType as r1Type, r2.RestaurantType as r2Type, ABS(r1.RestaurantsPriceRange2 - r2.RestaurantsPriceRange2) as PriceDiff,
       ABS(r1.Rating - r2.Rating) as RatingDiff
       FROM Restaurant r1 JOIN Restaurant r2 ON r1.Site != r2.SimilarRest1 AND r1.Site != r2.SimilarRest2 AND r1.Site != r2.SimilarRest3 AND r1.Site != r2.Site
       AND DISTANCE(r1.Latitude, r1.Longitude, r2.Latitude, r2.Longitude) < 0.1
       ;''',db.cnx)
    df_nomatch['Match'] = np.zeros(len(df_nomatch))

    df = df_match.append(df_nomatch)

    df = helper.transform(df)

    X = helper.BuildX(df)
    y = df['Match'].values

    from sklearn import linear_model
    logit = linear_model.LogisticRegression()
    logit.fit(X, y)
    joblib.dump(logit, "data/logit.joblib.pkl", compress=9)    
    print cross_validation.cross_val_score(logit, X, y, cv=5)    

if __name__=='__main__':
    main()
