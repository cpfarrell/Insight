var markers = [];
var iterator = 0;
var geocoder;
var map;
var waypoints;
var longitude;
var latitude;
var location;

var restaurant_latlong = [];
var parsedJson;

var infowindow = new google.maps.InfoWindow();

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
	    deleteMarkers()
	    parsedJson = eval(result);
	    console.log("The output" + parsedJson)
	    console.log(parsedJson)
	    names = "<br>Top restaurants:<br>"
		//coordinates = []
	    avg_latitude = 0
	    avg_longitude = 0
	    count = 0
	    console.log(parsedJson.length)
	    for(var i = 0; i < parsedJson.length; i++) {
		//for (pair in parsedJson) {
		names = names + (parseInt(i)+1) + ". " + parsedJson[i]['Name'] + "<br>"
		console.log("Latitude " + parsedJson[i]['Latitude'])
		avg_latitude += parsedJson[i]['Latitude']
		avg_longitude +=parsedJson[i]['Longitude']
		count += 1
	    }
	    avg_latitude = avg_latitude/count
            avg_longitude = avg_longitude/count
	    console.log(avg_latitude + " " + avg_longitude)
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
	zoom: 13
    }
    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
}
      
function createMarkerlist(){
    console.log("Creating markers")
    console.log(parsedJson.length)
    for(var i = 0; i < parsedJson.length; i++) {
	//for (pair in parsedJson) {
	console.log("Latitude " + parsedJson[i]["Latitude"] + " Longitude " + parsedJson[i]["Lxongitude"])
	restaurant_latlong.push(new google.maps.LatLng(parsedJson[i]["Latitude"], parsedJson[i]["Longitude"]))
    }
    console.log("Creating new Marker List")
	}
      
function drop() {
        createMarkerlist()
        for (var i = 0; i < parsedJson.length; i++) {
	    setTimeout(function() {
		    addMarker(i);
		}, i * 200);
        }
}

function addMarker() {
    var html = '<div id="infowindow">';
    html += "Name: " + parsedJson[iterator]["Name"] + "<br>Most similar items: " + parsedJson[iterator]["Words"]
    html +='</div>';
    var image = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+parseInt(iterator+1) + '|FE6256|000000';
    console.log(image)
    var marker = new google.maps.Marker({
	    //position: new google.maps.LatLng(parsedJson[iterator]["Latitude"], parsedJson[iterator]["Longitude"]),
	    position: restaurant_latlong[iterator],
	    map: map,
	    draggable: false,
	    icon: image,
	    animation: google.maps.Animation.DROP,
	    title:"Restaurant #" + (parseInt(iterator+1))
	});
    markers.push(marker)
	google.maps.event.addListener(marker, 'click', function() {
	    infowindow.setContent(html);
	    infowindow.open(map,marker);
	});
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
    parsedJson = []
	//restaurant_latlong = [];
    markers = [];
    iterator = 0;
    console.log("Deleting markers")
	}
    
function setAllMap(map) {
    for (var i = 0; i < markers.length; i++) {
	markers[i].setMap(map);
    }
}
