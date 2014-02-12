import redis_database

redis_db = redis_database.RedisDatabase()

chicago = [
"chicago"
]

boston = [
"boston"
]

philadelphia = [
"philadelphia"
]

tampa = [
"tampa",
"soho%2C+tampa",
"west+tampa",
"south+tampa",
"Carrollwood%2C+Tampa+Bay%2C+FL",
"Town+N+Country%2C+Tampa+Bay%2C+FL",
"Temple+Terrace%2C+Tampa+Bay%2C+FL",
"Downtown+Tampa%2C+Tampa+Bay%2C+FL",
"Ybor+City%2C+Tampa+Bay%2C+FL",
"Brandon%2C+Tampa+Bay%2C+FL",
"st+pete%2C+fl",
"St+Pete+Beach%2C+Tampa+Bay%2C+FL",
"Largo%2C+Tampa+Bay%2C+FL",
"Clearwater%2C+Tampa+Bay%2C+FL",
"Clearwater+Beach%2C+Tampa+Bay%2C+FL",
"Palm+Harbor%2C+Tampa+Bay%2C+FL"
]

ny = [
"Manhattan%2C+NY",
"Brooklyn%2C+NY",
"Queens%2C+NY",
"Bronx%2C+NY",
"Staten+Island%2C+NY",
"Long+Island+City%2C+Queens%2C+NY"
]

sf = [
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
"Outer+Mission%2C+San+Francisco%2C+CA"
"Financial+District%2C+San+Francisco%2C+CA",
"North+Beach%2FTelegraph+Hill%2C+San+Francisco%2C+CA",
"Alamo+Square%2C+San+Francisco%2C+CA",
"Anza+Vista%2C+San+Francisco%2C+CA",
"Ashbury+Heights%2C+San+Francisco%2C+CA",
"Balboa+Terrace%2C+San+Francisco%2C+CA",
"Bayview-Hunters+Point%2C+San+Francisco%2C+CA",
"Chinatown%2C+San+Francisco%2C+CA",
"Civic+Center%2C+San+Francisco%2C+CA",
"Cole+Valley%2C+San+Francisco%2C+CA",
"Corona+Heights%2C+San+Francisco%2C+CA",
"Diamond+Heights%2C+San+Francisco%2C+CA",
"Dogpatch%2C+San+Francisco%2C+CA",
"Embarcadero%2C+San+Francisco%2C+CA",
"Fillmore%2C+San+Francisco%2C+CA",
"Fisherman's+Wharf%2C+San+Francisco%2C+CA",
"Forest+Hill%2C+San+Francisco%2C+CA",
"Glen+Park%2C+San+Francisco%2C+CA",
"Hayes+Valley%2C+San+Francisco%2C+CA",
"Ingleside%2C+San+Francisco%2C+CA",
"Inner+Richmond%2C+San+Francisco%2C+CA",
"Inner+Sunset%2C+San+Francisco%2C+CA",
"Japantown%2C+San+Francisco%2C+CA",
"Laurel+Heights%2C+San+Francisco%2C+CA",
"Lower+Haight%2C+San+Francisco%2C+CA",
"Marina%2C+San+Francisco%2C+CA",
"Merced+Heights%2C+San+Francisco%2C+CA",
"Miraloma+Park%2C+San+Francisco%2C+CA",
"Mission+Bay%2C+San+Francisco%2C+CA",
"Mission+Terrace%2C+San+Francisco%2C+CA",
"Monterey+Heights%2C+San+Francisco%2C+CA",
"Mount+Davidson+Manor%2C+San+Francisco%2C+CA",
"NoPa%2C+San+Francisco%2C+CA",
"Nob+Hill%2C+San+Francisco%2C+CA",
"Noe+Valley%2C+San+Francisco%2C+CA",
"Oceanview%2C+San+Francisco%2C+CA",
"Pacific+Heights%2C+San+Francisco%2C+CA",
"Parkside%2C+San+Francisco%2C+CA",
"Portola%2C+San+Francisco%2C+CA",
"Potrero+Hill%2C+San+Francisco%2C+CA",
"Presidio%2C+San+Francisco%2C+CA",
"Russian+Hill%2C+San+Francisco%2C+CA",
"Sea+Cliff%2C+San+Francisco%2C+CA",
"Sherwood+Forest%2C+San+Francisco%2C+CA",
"SoMa%2C+San+Francisco%2C+CA",
"St+Francis+Wood%2C+San+Francisco%2C+CA",
"Stonestown%2C+San+Francisco%2C+CA",
"Sunnyside%2C+San+Francisco%2C+CA",
"Tenderloin%2C+San+Francisco%2C+CA",
"The+Haight%2C+San+Francisco%2C+CA",
"Twin+Peaks%2C+San+Francisco%2C+CA",
"Union+Square%2C+San+Francisco%2C+CA",
"Visitacion+Valley%2C+San+Francisco%2C+CA",
"West+Portal%2C+San+Francisco%2C+CA",
"Western+Addition%2C+San+Francisco%2C+CA",
"Westwood+Highlands%2C+San+Francisco%2C+CA",
"Westwood+Park%2C+San+Francisco%2C+CA"
]

bayarea = [
"mountain+view",
"palo+alto",
"san+jose",
"redwood+city",
"cupertino",
"santa+clara",
"san+mateo",
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
]


la = [
"santa+monica",
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
"West+Covina%2C+CA",
"Anaheim%2C+CA",
"Norwalk%2C+CA",
"Hawthorne%2C+CA",
"Compton%2C+CA",
"Manhattan+Beach%2C+CA",
]

def main():
    neighborhoods = sf
    sf.extend(bayarea)
    sf.extend(la)
    sf.extend(ny)
    sf.extend(tampa)
    sf.extend(chicago)
    sf.extend(boston)
    sf.extend(philadelphia)

    for neighborhood in neighborhoods:
        redis_db.add_to_group("neighborhoods", neighborhood)

if __name__ == '__main__':
    main()
