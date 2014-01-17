import numpy as np

def BuildX(df):
    columns = ['TypeMatches', 'PriceDiff', 'RatingDiff', 'MealSame', 'TableSame']
    X = np.ones(shape=(len(df),len(columns)+1))
    X[:,range(1,len(columns)+1)] = df[columns].values
    return X

def transform(df):
    count_matches(df, 'Type')
    count_matches(df, 'Food')
    count_close(df)
    return df

def count_matches(df, column):
    df['r1'+column] = df['r1'+column].map(lambda x: x.split('---'))
    df['r2'+column] = df['r2'+column].map(lambda x: x.split('---'))
    df[column+'Matches'] = df.apply(sum_types, args=(column,), axis=1)
    return df

def sum_types(row, column):
    count = 0
    for rType in row['r1'+column]:
        if rType in row['r2'+column]:
            count += 1
    return count

def count_close(df):
    df['TypeCloseMatches'] = df.apply(sum_close_types, axis=1)
    return df

def sum_close_types(row):
    count = 0
    for rType1 in row['r1Type']:
        for rType2 in row['r2Type']:
            if (rType1,rType2) in close_matches or (rType2,rType1) in close_matches:
                count += 1
    return count

close_matches = set([
("Japanese", "Sushi Bars"), 
("Delis", "Sandwiches"), 
("Italian", "Pizza"), 
("American (New)", "Breakfast & Brunch"), 
("American (Traditional)", "Breakfast & Brunch"), 
("American (New)", "American (Traditional)"), 
("American (New)", "Bars"), 
("Coffee & Tea", "Sandwiches"), 
("Breakfast & Brunch", "Coffee & Tea"), 
("Breakfast & Brunch", "Diners"), 
("Burgers", "Fast Food"), 
("American (New)", "Italian"), 
("Mediterranean", "Middle Eastern"), 
("American (New)", "Burgers"), 
("American (New)", "Sandwiches"), 
("Cafes", "Coffee & Tea"), 
("Cafes", "Sandwiches"), 
("American (New)", "French"), 
("Breakfast & Brunch", "Cafes"), 
("American (New)", "Seafood"), 
("American (Traditional)", "Burgers"), 
("Breakfast & Brunch", "Sandwiches"), 
("Indian", "Pakistani"), 
("Indian", "Vegetarian"), 
("Asian Fusion", "Japanese"), 
("American (Traditional)", "Diners"), 
("Asian Fusion", "Chinese"), 
("Salad", "Sandwiches"), 
("Caterers", "Sandwiches"), 
("Vegan", "Vegetarian"), 
("American (New)", "Wine Bars"), 
("Burgers", "Sandwiches"), 
("Greek", "Mediterranean"), 
("Breakfast & Brunch", "Burgers"), 
("Breakfast & Brunch", "French"), 
("American (New)", "Mediterranean"), 
("American (New)", "Lounges"), 
("Food Stands", "Mexican"), 
("American (New)", "Cafes"), 
("Latin American", "Mexican"), 
("Breakfast & Brunch", "Mexican"), 
("Barbeque", "Korean"), 
("Caterers", "Delis"), 
("Sandwiches", "Vietnamese"), 
("Asian Fusion", "Sushi Bars"), 
("American (Traditional)", "Sandwiches"), 
("Italian", "Sandwiches"), 
("Fast Food", "Mexican"), 
("Middle Eastern", "Persian/Iranian"), 
("Seafood", "Steakhouses"), 
("Italian", "Seafood"), 
("American (Traditional)", "Italian"), 
("American (New)", "Pubs"), 
("American (New)", "Coffee & Tea"), 
("Fish & Chips", "Seafood"), 
("Cheesesteaks", "Sandwiches"), 
("American (Traditional)", "Bars"), 
("American (New)", "Pizza"), 
("Breakfast & Brunch", "Creperies"), 
("American (New)", "Vegetarian"), 
("French", "Italian"), 
("Italian", "Wine Bars"), 
("American (New)", "Gastropubs"), 
("Mexican", "Seafood"), 
("Chinese", "Taiwanese"), 
("Bars", "Mexican"), 
("Pizza", "Sandwiches"), 
("Bakeries", "Sandwiches"), 
("Coffee & Tea", "Delis"), 
("Bars", "Breakfast & Brunch"), 
("Breakfast & Brunch", "Italian"), 
("Chinese", "Seafood"), 
("American (New)", "Asian Fusion"), 
("Bakeries", "Breakfast & Brunch"), 
("American (New)", "Delis"), 
("Chinese", "Japanese"), 
("Cajun/Creole", "Seafood"), 
("American (New)", "Mexican"), 
("American (New)", "Salad"), 
("Asian Fusion", "Thai"), 
("Gluten-Free", "Pizza"), 
("Barbeque", "Caterers"), 
("Bars", "Italian"), 
("Halal", "Indian"), 
("Chinese", "Dim Sum"), 
("American (Traditional)", "Pubs"), 
("Caterers", "Mexican"), 
("Mediterranean", "Turkish"), 
("Burgers", "Diners"), 
("Cafes", "Delis"), 
("Chinese", "Fast Food"), 
("American (New)", "Diners"), 
("American (Traditional)", "Seafood"), 
("Grocery", "Mexican"), 
("American (Traditional)", "Cafes"), 
("American (Traditional)", "Coffee & Tea"), 
("Bars", "Lounges"), 
("American (Traditional)", "French"), 
("Chinese", "Shanghainese"), 
("Barbeque", "Chinese")])
