#Standard modules
import json
from collections import defaultdict

#Third party modules
from pandas import DataFrame
import numpy as np
import pandas
from sklearn import linear_model
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

#My modules
import helper
import sql_database
db = sql_database.DbAccess('YELP', usr='root')

stop_words = ['west', 'east', 'north', 'south', 'mission', 'la', 'httpwwwyelpcombiz', 'food', 'place', 'dish', 'good', 'newsentencebegin', 'NEWREVIEW', 'newreview', 'like']

n_restaurants = 5

#Find the next most common word, but check to make sure it is not a subword of something we already have
def next_word(words, indices, ngrams):
    for index in indices:
        new = True
        for idx, word in enumerate(words):
            if ngrams[index] in word or word in ngrams[index]:
                #Generally, the longer the ngram the better so lets replace the earlier one if we have something longer
                if len(ngrams[index])>len(word):
                    words[idx] = ngrams[index]
                new = False
        if new:
            return ngrams[index]

def tf_idf(df, r1Reviews, r2Review):
    Reviews = r1Reviews
    Reviews.append(r2Review)
    Reviews = [Review[1] for Review in Reviews]

    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=1.0, stop_words='english', ngram_range=(1,2))
    r2_ngrams = vectorizer.fit(r2Review).get_feature_names()
    r2_ngrams = [ngram for ngram in r2_ngrams if not any(word in stop_words for word in ngram.split())]    

    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=1.0, stop_words='english', ngram_range=(1,2), vocabulary=r2_ngrams)
    tfidf_counts = vectorizer.fit_transform(Reviews)
    r2 = tfidf_counts[-1,:]
    r1 = tfidf_counts[range(tfidf_counts.shape[0]-1),:]

    product = r1.multiply(r2).todense()
    cosine = r1.dot(r2.transpose()).todense()
    #cosine = np.sum(product)
    lengths = r1.sum(axis=1)
    similarity = np.divide(cosine, lengths).A1

    #max_indices = product.argmax(axis=1)
    product_sort = (-product).argsort(axis=1)
    max_words = [next_word([], product_sort[idx,:].A1, r2_ngrams) for idx in range(product_sort.shape[0])]
    max_words2 = [next_word([max_words[idx]], product_sort[idx,:].A1, r2_ngrams) for idx in range(product_sort.shape[0])]
    max_words3 = [next_word([max_words[idx], max_words2[idx]], product_sort[idx,:].A1, r2_ngrams) for idx in range(product_sort.shape[0])]

    df['max_words'] = max_words
    df['max_words2'] = max_words2
    df['max_words3'] = max_words3
    df['similarity'] = similarity
    df = df.sort('similarity', ascending=False).reset_index()

    return df

def predict_rest(restaurant, miles, zipcode):
    df = pandas.io.sql.read_frame('''
     SELECT r1.Name as r1Name, r1.FullName as r1FullName, r1.RestaurantType as r1Type, r1.Site as r1Site, 
     r1.Street as r1Street, r1.City as r1City, r1.State as r1State, r1.Zip as r1Zip, r1.Phone as r1Phone,
     r2.RestaurantType as r2Type, ABS(r1.RestaurantsPriceRange2 - r2.RestaurantsPriceRange2) as PriceDiff,
     ABS(r1.Rating - r2.Rating) as RatingDiff, r1.Latitude as Latitude, r1.Longitude as Longitude, r1.GoodForMeal=r2.GoodForMeal as MealSame,
     r1.RestaurantsTableService=r2.RestaurantsTableService as TableSame, r1.Favorites as r1Food, r2.Favorites as r2Food '''
     '''FROM Restaurant r1 JOIN ZipCodes
     ON DISTANCE(ZipCodes.Latitude, ZipCodes.Longitude, r1.Latitude, r1.Longitude) < ''' + miles + ''' CROSS JOIN Restaurant r2
     WHERE (r2.FullName = "''' + restaurant + '''" OR r2.Site = "''' + restaurant + '''") AND ZipCodes.Zip = ''' + zipcode + ''' AND r1.NReviews > 100;'''
                                  , db.cnx)

    if len(df)==0:
        return []

    df = helper.transform(df)

    #Use logistic regression to reduce list of possible restaurants
    X = helper.BuildX(df)
    logistic = joblib.load("data/logit.joblib.pkl")
    df['scores'] = logistic.decision_function(X)
    df = df.sort('scores', ascending=False).reset_index()
    df = df.ix[range(50),:]
    #df=df.ix[df['scores']>4]

    #Sort by name to keep aligned
    df = df.sort('r1FullName')

    #Grab reviews from those restaurants. Python sort instead of SQL ORDER BY because of different treatment of capitalized letters
    r1FullNames = '", "'.join(df['r1FullName'].tolist())
    db.cursor.execute('SELECT FullName, Review FROM Restaurant WHERE FullName IN ("' + r1FullNames + '") AND NReviews > 100 ORDER BY FullName;')
    r1Reviews = db.cursor.fetchall()
    r1Reviews = sorted(r1Reviews)

    db.cursor.execute('SELECT FullName, Review FROM Restaurant WHERE (FullName = "' + restaurant + '" OR Site = "' + restaurant + '");')
    r2Review = db.cursor.fetchone()

    df = tf_idf(df, r1Reviews, r2Review)

    restaurants = []
    for i in range(n_restaurants):
        restaurants.append({'Name' :df.ix[i, 'r1Name'], 'Words': (df.ix[i, 'max_words'] + ', ' + df.ix[i, 'max_words2'] + ', ' + df.ix[i, 'max_words3']),
                            'Street': df.ix[i, 'r1Street'], 'City': df.ix[i, 'r1City'] + ', ' + df.ix[i, 'r1State'] + ' ' + df.ix[i, 'r1Zip'],  'Phone': df.ix[i, 'r1Phone'],
                            'Site': df.ix[i, 'r1Site'], 'Latitude': df.ix[i, 'Latitude'], 'Longitude': df.ix[i, 'Longitude']})

    return restaurants

if __name__=='__main__':
    print predict_rest("Fat Sal's Deli 972 Gayley Ave Los Angeles, CA 90024", "10", "94117")
#    print predict_rest("/biz/tender-greens-hollywood", "5", "95135")
