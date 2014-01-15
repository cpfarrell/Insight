import redis_database

redis_db = redis_database.RedisDatabase()

neighborhoods = [
"mountain+view",
"santa+monica",
"palo+alto",
"san+jose",
"redwood+city",
"cupertino",
"santa+clara",
"san+mateo",
"Westwood%2C+Los+Angeles%2C+CA",
"Venice%2C+CA",
"90025",
"Culver+City%2C+CA",
"Marina+del+Rey%2C+CA",
"Hollywood%2C+Los+Angeles%2C+CA",
"West+Hollywood%2C+Los+Angeles%2C+CA",
"Los+Angeles%2C+CA",
"Van+Nuys%2C+CA",
"Burbank%2C+CA",
"Pasadena%2C+CA",
"Glendale%2C+CA",
"Torrance%2C+CA",
"Long+Beach%2C+CA",
"South+Los+Angeles%2C+Los+Angeles%2C+CA",
"West+Covina%2C+CA",
"Anaheim%2C+CA",
"Norwalk%2C+CA",
"Huntington+Beach%2C+CA",
"Irvine%2C+CA",
"Santa+Ana%2C+CA",
"Hawthorne%2C+CA",
"Compton%2C+CA",
"Manhattan+Beach%2C+CA",
"Ontario%2C+CA",
"Riverside%2C+CA",
"San+Bernardino%2C+CA",
"Chino+Hills%2C+CA",
"south+san+francisco",
"mission%2C+san+francisco",
"san+francisco",
"downtown+san+francisco",
"SoMa%2C+San+Francisco%2C+CA",
"Market%2C+San+Francisco%2C+CA",
"Bernal+Heights%2C+San+Francisco%2C+CA",
"Marina%2FCow+Hollow%2C+San+Francisco%2C+CA",
"Castro%2C+San+Francisco%2C+CA",
"Bayview-Hunters+Point%2C+San+Francisco%2C+CA",
"Daly+City",
"Alameda",
"Oakland",
"Berkeley",
"San+Leandro",
"Hayward",
"Fremont%2C+CA",
"Milpitas%2C+CA",
"Oceanside%2C+CA",
"Escondido%2C+C",
"Encinitas%2C+CA",
"La+Jolla%2C+CA",
"Mission+Beach%2C+CA",
"San+Diego%2C+CA",
"Chula+Vista%2C+CA",
"La+Mesa%2C+CA",
"Santa+Barbara%2C+CA",
"Malibu%2C+CA",
"Fresno%2C+CA",
"Bakersfield%2C+CA",
"Santa+Cruz%2C+CA",
"Monterey%2C+CA",
"Sacramento%2C+CA",
"Rancho+Cordova%2C+CA",
"Arden-Arcade%2C+Sacramento%2C+CA",
"Citrus+Heights%2C+CA",
]

#for neighborhood in neighborhoods:
#    redis_db.add_to_group("neighborhoods", neighborhood)

print "DEBUG1"
print len(redis_db.get_members("restaurant_searched"))
count = 0
for restaurant in redis_db.get_members("restaurant_searched"): 
    count +=1
    if count %100==0:
        print count
    matched_neighs = [neighborhood for neighborhood in neighborhoods if redis_db.is_member(neighborhood, restaurant)]
    redis_db.add_info(restaurant, {"neighborhoods": matched_neighs})
print "DEBUG2"
for restaurant in redis_db.get_members("restaurant_to_search"):
    matched_neighs = [neighborhood for neighborhood in neighborhoods if redis_db.is_member(neighborhood, restaurant)]
    redis_db.add_info(restaurant, {"neighborhoods": matched_neighs})
print "DEBUG3"
