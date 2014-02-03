import json
import operator
import cPickle
import timeit
from collections import defaultdict
import glob

#Third party modules
from pandas import DataFrame
import pandas
from scipy.sparse import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

import stopwords
sw = stopwords.StopWords()
stop_words = sw.get_words()
import sql_database
db = sql_database.DbAccess('INSIGHT', usr='root')

vectorizer = CountVectorizer(max_df=1.0, stop_words='english', ngram_range=(1,2))

def build_tokens(Review):
    tokens = Review.split()
    tokens = [token for token in tokens if token not in stop_words]
    tokens.extend([tokens[j] + " " + tokens[j+1] for j in range(len(tokens)-1)])
    tokens = [token for token in tokens if len(token)<18]
    return tokens

def count_list(ngrams):
    result = defaultdict(int)
    for ngram in ngrams:
        result[ngram] += 1
    return result

def make_token_db(df):
    count = 0
    word_tokens = {}
    for idx, restaurant in enumerate(restaurants):
        if idx%100==0:
            print idx

        sql = ('SELECT Review FROM Restaurant WHERE FullName = "' + restaurant + '";')
        db.cursor.execute(sql)
        Review = db.cursor.fetchall()[0][0]

        tokens = build_tokens(Review)
        for token in tokens:
            if token not in word_tokens:
                word_tokens[token] = count
                count += 1

    print "Writing to file"
    print len(word_tokens)
    f = open('/usr/local/mysql/data/token_files/tokens_0.txt', 'w')
    for idx, token in enumerate(word_tokens):
        f.write(str(word_tokens[token]) + '\t"' + token + '"\n')

        if idx%10000==0 and idx>0:
            f.close()
            f = open('/usr/local/mysql/data/token_files/tokens_' + str(idx/10000) + '.txt', 'w')

    with open('data/word_tokens.pkl', 'wb') as fid:
        print "Trying to dump to pickle"
        cPickle.dump(word_tokens, fid)
        print "Done with pickle"

def load_table():
    db.cursor.execute('DROP TABLE IF EXISTS Token;')
    db.cursor.execute('CREATE TABLE Token (ID INTEGER PRIMARY KEY, Word CHAR(30));')

    files = glob.glob('/usr/local/mysql/data/token_files/tokens_*.txt')
    for file in files:
        db.cursor.execute('LOAD DATA INFILE "' + file + '" INTO TABLE Token;')
        db.commit()

def build_matrix(df):
    print 'Building matrix'

    with open('data/word_tokens.pkl') as fid:
        word_tokens = cPickle.load(fid)

    sql = ('SELECT MAX(ID)+1 FROM Restaurant;')
    db.cursor.execute(sql)
    n_rests = db.cursor.fetchall()[0][0]
    print 'Total number of restaurants ' + str(n_rests)

    n_tokens = len(word_tokens)
    print 'Total number of tokens ' + str(n_tokens)

    row = []
    col = []
    data = []
    for idx, restaurant in enumerate(restaurants):
        if idx%100==0:
            print idx

        sql = ('SELECT Review, ID FROM Restaurant WHERE FullName = "' + restaurant + '";')
        db.cursor.execute(sql)
        results = db.cursor.fetchall()
        Review = results[0][0]
        ID_rest = results[0][1]

        tokens = build_tokens(Review)
        tokens = count_list(tokens)
        
        for token in tokens:
            if token in word_tokens:
                row.append(ID_rest)
                col.append(word_tokens[token])
                data.append(tokens[token])

    X = coo_matrix((data,(row,col)))

    print "Done creating matrix"
    X = X.tocsr()
    print "Writing to pickle"

    with open('data/word_matrix.pkl', 'wb') as fid:
        cPickle.dump(X, fid)

if __name__=='__main__':
    print "Loading reviews"
    sql = ('SELECT FullName FROM Restaurant')
    db.cursor.execute(sql)
    restaurants = [restaurant[0] for restaurant in db.cursor.fetchall()]
    print "Have reviews from " + str(len(restaurants)) + " restaurants"
    #make_token_db(restaurants)
    print "Built token db"
    #load_table()
    print 'Loaded table'
    build_matrix(restaurants)
