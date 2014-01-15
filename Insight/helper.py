import numpy as np

def BuildX(df):
    X = np.ones(shape=(len(df),4))
    X[:,range(1,4)] = df[['TypeMatches', 'PriceDiff', 'RatingDiff']].values
    return X

def transform(df):
    df['r1Type'] = df['r1Type'].map(lambda x: x.split('---'))
    df['r2Type'] = df['r2Type'].map(lambda x: x.split('---'))
    df['TypeMatches'] = df.apply(sum_types, axis=1)
    return df

def sum_types(row):
    count = 0
    for rType in row['r1Type']:
        if rType in row['r2Type']:
            count += 1
    return count
