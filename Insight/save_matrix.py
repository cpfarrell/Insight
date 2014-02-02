import json
import operator
import cPickle

#Third party modules
from pandas import DataFrame
import pandas
from scipy.sparse import *
from sklearn.feature_extraction.text import TfidfVectorizer

#My modules                                                                                                                                                                          
import sql_database
db = sql_database.DbAccess('INSIGHT', usr='root')

stop_words = set(['west', 'east', 'north', 'south', 'mission', 'la', 'httpwwwyelpcombiz', 'food', 'place', 'dish', 'good', 'newsentencebegin', 'NEWREVIEW', 'newreview', 'like',
              'really', 'great', 'menu', 'restaurant', 'santa', 'monica', 'groupon', 'happy', 'hour', 'tony', 'rag', 'httpwwwyelpcomuser', 'waitress', 'valet', 'michelin'
              , 'james', 'beard', 'del'])

vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=1.0, stop_words='english', ngram_range=(1,2))

def make_token_db(df):
    db.cursor.execute('DROP TABLE IF EXISTS Token;')
    db.cursor.execute('CREATE TABLE Token (Word CHAR(80) NOT NULL PRIMARY KEY, ID INTEGER);')

    count = 0
    for i in range(len(df)):
        if i%10==0:
            print i
        Review = df.ix[i, 'Review']
        tokens = vectorizer.fit([Review]).get_feature_names()
        for token in tokens:
            sw = False
            for word in token.split():
                if word in stop_words:
                    sw = True
            if sw:
                continue

            if token not in stop_words:
                db.cursor.execute('SELECT COUNT(*) FROM Token WHERE Word = "' + token + '";')
                entries = db.cursor.fetchall()[0][0]
                if entries == 0:
                    try: 
                        db.cursor.execute('INSERT INTO Token (Word, ID) VALUES ("' + token + '", ' + str(count) + ');')
                        db.commit()
                    except:
                        print token
                    count += 1


def build_matrix(df):
    print 'Building matrix'

    sql = ('SELECT MAX(ID)+1 FROM Restaurant;')
    db.cursor.execute(sql)
    n_rests = db.cursor.fetchall()[0][0]
    print 'Total number of restaurants ' + str(n_rests)

    sql = ('SELECT MAX(ID)+1 FROM Token;')
    db.cursor.execute(sql)
    n_tokens = db.cursor.fetchall()[0][0]
    print 'Total number of tokens ' + str(n_tokens)

    X = lil_matrix((n_rests, n_tokens))

    for i in range(len(df)):
        if i%10==0:
            print i
        Review = df.ix[i, 'Review']
        ID_rest = df.ix[i, 'ID']
        tokens = vectorizer.fit([Review]).get_feature_names()
        for token in tokens:
            if token in stop_words:
                continue

            db.cursor.execute('SELECT ID FROM Token WHERE Word = "' + token + '";')
            results = db.cursor.fetchall()
            if len(results)>0:
                ID_token = results[0][0]
                X[ID_rest, ID_token] += 1

    print "Done creating matrix"
    X = X.tocsr()
    print "Writing to pickle"

    with open('data/word_matrix.pkl', 'wb') as fid:
        cPickle.dump(X, fid)

if __name__=='__main__':
    print "Loading reviews"
    df = pandas.io.sql.read_frame('SELECT FullName, ID, Review FROM Restaurant', db.cnx)
    print "Have reviews from " + str(len(df)) + " restaurants"
    make_token_db(df)
    print "Built token db"
    build_matrix(df)
