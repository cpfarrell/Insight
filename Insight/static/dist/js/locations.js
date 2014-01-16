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

// Javascript to get restaurant from page
function getRestaurant(restaurant, zipcode, miles) {
    //Log inputs to console
    console.log(("Input is restaurant = " + restaurant + ", miles = " + miles + " and zip = " + zipcode));
    //Go to the page /restaurant (see drive_app.py) and pass in the arguments restaurant and zipcode
    $.get('/restaurant?restaurant='+restaurant+'&miles='+miles+'&zip='+zipcode, function(result) {
	    //Log the output to console
	    console.log("Output is = " + result);
	    //Fill in the results that will go on the page
	    //var parsedJson = $.getJSON(result)
	    var parsedJson = eval(result);
	    names = "<br>Top restaurants:<br>"
	    coordinates = []
	    for (pair in parsedJson) {
		names = names + (parseInt(pair)+1) + ". " + parsedJson[pair][pair][0] + "<br>"
		coordinates.push({"Latitude": parsedJson[pair][pair][1], "Longitude": parsedJson[pair][pair][2]})
	    }
	    console.log("Coordinates1 " + coordinates)
	    drop()
	    $('#output_results').val(names);
	    $('#output_results').html(names);
	    //I don't think this returned value is used at all
	    return result;
	});
};

var sf = new google.maps.LatLng(37.7771187, -122.4196396);

function initialize(center) {
    geocoder = new google.maps.Geocoder();
    var mapOptions = {
	center: center,
	zoom: 10
    }
    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
}
      
function createMarkerlist(){
    //coordinates = document.getElementById("points").value
    //coordinates = points.value
    console.log("Coordinates " + coordinates)
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
		    addMarker();
		}, i * 200);
        }
}

function addMarker() {
    markers.push(new google.maps.Marker({
		position: restaurant_latlong[iterator],
		    map: map,
		    draggable: false,
		    animation: google.maps.Animation.DROP,
		    title:"Hello World"
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
google.maps.event.addDomListener(window, 'load', initialize(sf));