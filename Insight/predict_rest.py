#Standard modules
import json
from collections import defaultdict
import cPickle

#Third party modules
from pandas import DataFrame
import numpy as np
import pandas
from sklearn import linear_model
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from pygeocoder import Geocoder
import nltk

#My modules
import helper
import sql_database
db = sql_database.DbAccess('INSIGHT', usr='root')
afinn = dict(map(lambda (k,v): (k,int(v)), [ line.split('\t') for line in open("data/AFINN-111.txt") ]))

stop_words = ['west', 'east', 'north', 'south', 'mission', 'la', 'httpwwwyelpcombiz', 'food', 'place', 'dish', 'good', 'newsentencebegin', 'NEWREVIEW', 'newreview', 'like',
              'really', 'great', 'menu', 'restaurant', 'santa', 'monica', 'groupon', 'happy', 'hour', 'tony', 'rag', 'httpwwwyelpcomuser', 'waitress', 'valet', 'michelin'
              , 'james', 'beard', 'del']

n_restaurants = 5
print "Loading data"
with open('data/word_data.pkl') as fid:
    data = cPickle.load(fid)

print "Loading row"
with open('data/word_row.pkl') as fid:
    row = cPickle.load(fid)

print "Loading column"
with open('data/word_col.pkl') as fid:
    col = cPickle.load(fid)

print "Building matrix"
X = coo_matrix((data,(row,col))) 
print "Converting matrix"
X = X.tocsr()
print "Done"

def word_match(word1, word2):
    if any([any(nltk.metrics.edit_distance(s_word1, s_word2)<3 for s_word2 in word2.split()) for s_word1 in word1.split()]):
        return True
    return False

#Find the next most common word, but check to make sure it is not a subword of something we already have
def next_word(words, indices, ngrams):
    for index in indices:
        new = True
        replaced=False
        #Check if the next ngram is similar to previously found ones and if so don't use it
        for idx, word in enumerate(words):
            if word_match(ngrams[index], word):
                #Generally, the longer the ngram the better so lets replace the earlier one if we have something longer
                new = False
                if len(ngrams[index])>len(word):
                    words[idx] = ngrams[index]
                    #If ngram already swapped forward and another match occurs, then need to get unsimilar one
                    if replaced:
                        words = next_word(words[:idx], indices, ngrams).split('<br>')
                    replaced=True
                else:
                    break

        if new:
            words.append(ngrams[index])
            return '<br>'.join(words)

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

    product = np.multiply(r1.todense(), r2.todense())
    cosine = r1.dot(r2.transpose()).todense()
    #cosine = np.sum(product)
    lengths = np.sqrt(r1.multiply(r1).sum(axis=1))
    similarity = np.divide(cosine, lengths).A1

    #max_indices = product.argmax(axis=1)
    product_sort = (-product).argsort(axis=1)
    max_words = [next_word([], product_sort[idx,:].A1, r2_ngrams) for idx in range(product_sort.shape[0])]
    max_words = [next_word(max_words[idx].split('<br>'), product_sort[idx,:].A1, r2_ngrams) for idx in range(product_sort.shape[0])]
    max_words = [next_word(max_words[idx].split('<br>'), product_sort[idx,:].A1, r2_ngrams) for idx in range(product_sort.shape[0])]

    df['max_words'] = max_words
    #df['max_words2'] = max_words2
    #df['max_words3'] = max_words3
    df['similarity'] = similarity
    df = df.sort('similarity', ascending=False).reset_index()
    return df

def add_links(max_words, site):
    words_list = max_words.split('<br>')
    words_list = ['<a href=http://www.yelp.com' + site + '?q=' + '+'.join(word.split()) + ' target="_blank"><big><big>' + word + '</big></big></a>' for word in words_list]
    return '<br>'.join(words_list)

def add_sent(df, r1Reviews):
    print len(df)
    for line in range(len(df)):
        review = [r1[1] for r1 in r1Reviews if r1[0]==df.ix[line, 'r1FullName']][0]
        sents = []
        reviews = review.split('NEWREVIEW')
        for review in reviews:
            sents.extend(review.split('newsentencebegin'))
        mws = df.ix[line, 'max_words'].split("<br>")
        for mw in mws:
            print mw + ' ' + str(afinn_score(mw, sents))

def afinn_score(mw, sents):
    count = 0
    afinn_score = 0
    for sent in sents:
        words = sent.split()
        if mw in words:
            for word in words:
                if word in afinn:
                    afinn_score += afinn[word]
                    count += 1.
    if count > 0:
        return float(afinn_score)/count
    return 0

def predict_rest(restaurant, miles, zipcode):
    results = Geocoder.geocode(zipcode)
    latitude = str(results[0].coordinates[0])
    longitude = str(results[0].coordinates[1])

    df = pandas.io.sql.read_frame('''
     SELECT r1.Name as r1Name, r1.FullName as r1FullName, r1.RestaurantType as r1Type, r1.Site as r1Site, 
     r1.Street as r1Street, r1.City as r1City, r1.State as r1State, r1.Zip as r1Zip, r1.Phone as r1Phone,
     r2.RestaurantType as r2Type, ABS(r1.RestaurantsPriceRange2 - r2.RestaurantsPriceRange2) as PriceDiff,
     ABS(r1.Rating - r2.Rating) as RatingDiff, r1.Latitude as Latitude, r1.Longitude as Longitude, r1.GoodForMeal=r2.GoodForMeal as MealSame,
     r1.RestaurantsTableService=r2.RestaurantsTableService as TableSame, r1.Favorites as r1Food, r2.Favorites as r2Food '''
     '''FROM Restaurant r1 CROSS JOIN Restaurant r2
     WHERE DISTANCE(''' + latitude + ''', ''' + longitude + ''', r1.Latitude, r1.Longitude) < ''' + miles + '''
     AND r2.FullName = "''' + restaurant + '''" AND r1.NReviews > 0;'''
                                  , db.cnx)
    if len(df)==0:
        return []
    
    df = helper.transform(df)
    print len(df)
    #Use logistic regression to reduce list of possible restaurants
    X = helper.BuildX(df)
    logistic = joblib.load("data/logit.joblib.pkl")
    df['scores'] = logistic.decision_function(X)
    df = df.sort('scores', ascending=False).reset_index()

    keep = max(20, len(df.ix[df['scores']>0]))
    keep = min(400, keep)
    keep = min(keep, len(df))
    print keep
    df = df.ix[range(keep),:]

    #Sort by name to keep aligned
    df = df.sort('r1FullName')
    print len(df)
    #Grab reviews from those restaurants. Python sort instead of SQL ORDER BY because of different treatment of capitalized letters
    r1FullNames = '", "'.join(df['r1FullName'].tolist())

    db.cursor.execute('SELECT FullName, Review FROM Restaurant WHERE FullName IN ("' + r1FullNames + '") AND NReviews>0;')
    r1Reviews = db.cursor.fetchall()
    r1Reviews = sorted(r1Reviews)

    db.cursor.execute('SELECT FullName, Review FROM Restaurant WHERE (FullName = "' + restaurant + '" OR Site = "' + restaurant + '");')
    r2Review = db.cursor.fetchone()

    df = tf_idf(df, r1Reviews, r2Review)[:n_restaurants]

    restaurants = []
    for i in range(n_restaurants):
        max_words = df.ix[i, 'max_words']
        site = df.ix[i, 'r1Site']
        max_words = add_links(max_words, site)
        restaurants.append({'Name' :df.ix[i, 'r1Name'], 'Words': max_words,
                            'Street': df.ix[i, 'r1Street'], 'City': df.ix[i, 'r1City'] + ', ' + df.ix[i, 'r1State'] + ' ' + df.ix[i, 'r1Zip'],  'Phone': df.ix[i, 'r1Phone'],
                            'Site': site, 'Latitude': df.ix[i, 'Latitude'], 'Longitude': df.ix[i, 'Longitude']})

    return restaurants

if __name__=='__main__':
    print predict_rest("Hostaria del Piccolo 606 Broadway Santa Monica, CA 90401", "5", "San Francisco")
