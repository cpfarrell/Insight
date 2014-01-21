var markers = [];
var iterator = 0;
var geocoder;
var map;
var waypoints;
var longitude;
var latitude;
var location;
var coordinates = []

var restaurant_latlong = [];

function readInfo(latitudes, longitudes) {
    //var parsedJson = eval(info);
    console.log(latitudes)
    console.log(longitudes)
    for (pair in parsedJson) {
	names = names + (parseInt(pair)+1) + ". " + parsedJson[pair][pair][0] + "<br> " + parsedJson[pair][pair][1] + "<br>"
	avg_latitude += parsedJson[pair][pair][2]
	avg_longitude +=parsedJson[pair][pair][3]
	coordinates.push({"Latitude": parsedJson[pair][pair][2], "Longitude": parsedJson[pair][pair][3]})
	    }
}

// Javascript to get restaurant from page
function getRestaurant(restaurant, zipcode, miles) {
    //Log inputs to console
    console.log(("Input is restaurant = " + restaurant + ", miles = " + miles + " and zipcode = " + zipcode));
    //Go to the page /restaurant (see drive_app.py) and pass in the arguments restaurant and zipcode
    $.get('/restaurant?restaurant='+restaurant+'&miles='+miles+'&zipcode='+zipcode, function(result) {
	    //Log the output to console
	    console.log("Output is = " + result);
	    //Fill in the results that will go on the page
	    //var parsedJson = $.getJSON(result)
	    var parsedJson = eval(result);
	    console.log(parsedJson)
	    names = "<br>Top restaurants:<br>"
	    coordinates = []
	    avg_latitude = 0
	    avg_longitude = 0
	    for (pair in parsedJson) {
		names = names + (parseInt(pair)+1) + ". " + parsedJson[pair][pair][0] + "<br> " + parsedJson[pair][pair][1] + "<br>"
		avg_latitude += parsedJson[pair][pair][2]
		avg_longitude +=parsedJson[pair][pair][3]
		coordinates.push({"Latitude": parsedJson[pair][pair][2], "Longitude": parsedJson[pair][pair][3]})
	    }
	    avg_latitude = avg_latitude/parsedJson.length
            avg_longitude = avg_longitude/parsedJson.length
	    google.maps.event.addDomListener(window, 'load', initialize(new google.maps.LatLng(avg_latitude, avg_longitude)));
	    drop()
	    $('#output_results').val(names);
	    $('#output_results').html(names);
	    //I don't think this returned value is used at all
	    return result;
	});
};

function drawMaps(locations) {
    google.maps.event.addDomListener(window, 'load', initialize(new google.maps.LatLng(avg_latitude, avg_longitude)));
    drop()
}

function initialize(center) {
    geocoder = new google.maps.Geocoder();
    var mapOptions = {
	center: center,
	zoom: 10
    }
    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
}
      
function createMarkerlist(){
    for (pair in coordinates) {
	console.log("Latitude " + coordinates[pair]["Latitude"] + " Longitude " + coordinates[pair]["Longitude"])
	restaurant_latlong.push(new google.maps.LatLng(coordinates[pair]["Latitude"], coordinates[pair]["Longitude"]))
    }
    console.log("Creating new Marker List")
	}
      
function drop() {
    deleteMarkers()
        createMarkerlist()
        for (var i = 0; i < restaurant_latlong.length; i++) {
	    setTimeout(function() {
		    addMarker(i);
		}, i * 200);
        }
}

function addMarker() {
    markers.push(new google.maps.Marker({
		position: restaurant_latlong[iterator],
		    map: map,
		    draggable: false,
		    animation: google.maps.Animation.DROP,
		    title:"Restaurant #" + (parseInt(iterator+1))
		    }));
    iterator++;
    console.log("Adding markers.")
	}
      
function clearMarkers() {
    setAllMap(null);
    console.log("Clearing markers")
	}
      
// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
    clearMarkers();
    restaurant_latlong = [];
    markers = [];
    iterator = 0;
    console.log("Deleting markers")
	}
    
function setAllMap(map) {
    for (var i = 0; i < markers.length; i++) {
	markers[i].setMap(map);
    }
}
