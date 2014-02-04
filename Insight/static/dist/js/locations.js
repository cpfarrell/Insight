var markers = [];
var iterator = 0;
var geocoder;
var map;
var waypoints;
var longitude;
var latitude;
var location;

var parsedJson;

var infowindow = new google.maps.InfoWindow();
infowindow.setOptions({maxWidth: 500});
var map;

// Javascript to get restaurant from page
function getRestaurant(restaurant, zipcode, miles) {
    //Log inputs to console
    //restaurant = html_entity_decode(restaurant)
    restaurant = $('<div />').html(restaurant).text();
    restaurant = restaurant.replace("&","%26");
    restaurant = restaurant.replace("+","%2B");
    console.log(("Input is restaurant = " + restaurant + ", miles = " + miles + " and zipcode = " + zipcode));
    //Go to the page /restaurant (see drive_app.py) and pass in the arguments restaurant and zipcode
    console.log("/restaurant?restaurant="+restaurant+"&miles="+miles+"&zipcode="+zipcode)
    $.get("/restaurant?restaurant="+restaurant+"&miles="+miles+"&zipcode="+zipcode, function(result) {
	    //Log the output to console
	    console.log("Output is = " + result);
	    //Fill in the results that will go on the page
	    //var parsedJson = $.getJSON(result)
	    deleteMarkers()
	    parsedJson = eval(result);
	    console.log("The output" + parsedJson)
	    console.log(parsedJson)
	    names = "<big>Top Restaurants:<br>"
		//coordinates = []
	    avg_latitude = 0
	    avg_longitude = 0
	    console.log(parsedJson.length)
	    min_lat = 999999.
	    max_lat = -999999.
	    min_long = 999999.
	    max_long = -999999.
	    console.log("The result length is " + parsedJson.length)
	    if (parsedJson.length<2) {
		$('#output_results').val("No restaurants found. Currently OldFaveNewPlace only supports SF bay area (San Fran to San Jose to Oakland), Los Ang");
		//$('#output_results').html("No restaurants found. Currently OldFaveNewPlace only supports SF bay area (San Fran to San Jose to Oakland, Los AngYork City");
		$('#output_results').html(parsedJson[0]);
		return result
	    }

	    for(var i = 0; i < parsedJson.length; i++) {
		names = names + (parseInt(i)+1) + ". " + parsedJson[i]['Name'] + "<br>"
		if (parsedJson[i]['Latitude'] < min_lat) {min_lat = parsedJson[i]['Latitude']}
		if (parsedJson[i]['Latitude'] > max_lat) {max_lat = parsedJson[i]['Latitude']}
		if (parsedJson[i]['Longitude'] < min_long) {min_long = parsedJson[i]['Longitude']}
		if (parsedJson[i]['Longitude'] > max_long) {max_long = parsedJson[i]['Longitude']}
		avg_latitude += parsedJson[i]['Latitude']
		avg_longitude +=parsedJson[i]['Longitude']
	    }
	    avg_latitude = avg_latitude/parsedJson.length
            avg_longitude = avg_longitude/parsedJson.length
	    console.log(avg_latitude + " " + avg_longitude)
	    map.setCenter(new google.maps.LatLng(avg_latitude, avg_longitude));
	    console.log(max_long)
	    max_long = max_long + (max_long-min_long)*0.8
	    console.log(max_long)
	    var bounds = new google.maps.LatLngBounds(new google.maps.LatLng(min_lat, min_long),new google.maps.LatLng(max_lat, max_long));
	    map.fitBounds(bounds);
	    document.getElementById("spinnerContainer").style.visibility = "hidden";
	    drop()
	    $('#output_results').val(names + "</big>");
	    $('#output_results').html(names + "</big>");
	    //I don't think this returned value is used at all
	    return result;
	});
};

function initialize() {
    geocoder = new google.maps.Geocoder();
    var mapOptions = {
	center: new google.maps.LatLng(37.7712, -122.4413),
	zoom: 13
    }
    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
    console.log('Besflkdadf')
}
      
function drop() {
        for (var i = 0; i < parsedJson.length; i++) {
	    setTimeout(function() {
		    addMarker(i);
		}, i * 200);
        }
	setAllMap(map)
}



function addMarker() {
    var html = '<div id="infowindow" style="width:170px">';
    html += "<big><big>Similar items:<br>" + parsedJson[iterator]["Words"] + "<br><br></big></big>"
    html += parsedJson[iterator]["Name"] + "<br>" + parsedJson[iterator]["Street"] + "<br>" + parsedJson[iterator]["City"] + "<br>"
    html += parsedJson[iterator]["Phone"] + "<br><a href=http://www.yelp.com" + parsedJson[iterator]["Site"] + " target='_blank'>See on yelp</a>"
    html +='</div>';
    var image = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+parseInt(iterator+1) + '|FE6256|000000';
    console.log(image)
    var marker = new google.maps.Marker({
	    position: new google.maps.LatLng(parsedJson[iterator]["Latitude"], parsedJson[iterator]["Longitude"]),
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
    markers = [];
    iterator = 0;
    console.log("Deleting markers")
	}
    
function setAllMap(map) {
    for (var i = 0; i < markers.length; i++) {
	markers[i].setMap(map);
    }
}

function showSearchPane() {
    document.getElementById('results').style.visibility='visible';
}
