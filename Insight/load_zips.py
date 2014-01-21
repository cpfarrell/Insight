import sql_database
db = sql_database.DbAccess('YELP', usr='root')
db.cursor.execute('DROP TABLE IF EXISTS ZipCodes;')
db.cursor.execute('CREATE TABLE ZipCodes (Zip INT, Latitude FLOAT, Longitude FLOAT)')

f = open('data/US.txt', 'r')
zip_location = {}
for idx, line in enumerate(f):
    values = line.split()
    zip_location[values[1]] = (values[-2], values[-1])

for zip in zip_location:
    Command = 'INSERT INTO ZipCodes (Zip, Latitude, Longitude) VALUES'
    Command += ' (' + str(zip) + ', ' + str(zip_location[zip][0]) + ', ' + str(zip_location[zip][1]) + ');'
    db.cursor.execute(Command)

db.commit()
