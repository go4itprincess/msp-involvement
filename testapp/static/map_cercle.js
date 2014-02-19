var map = L.map('map').setView([56.834, -3.994], 7);

// add an OpenStreetMap tile layer
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

var constituencies = [];
var circle = [];

$.getJSON("constituencies_geometry.js", function (data) {
    constituencies = data;

    for(var i = 0; i<Object.keys(constituencies).length; i++){
    	console.log([constituencies[i].geometry.centre_lat, constituencies[i].geometry.centre_lon], constituencies[i].geometry.area/100000);
        circle[i] = L.circle([constituencies[i].geometry.centre_lat, constituencies[i].geometry.centre_lon], constituencies[i].geometry.area/100000, {
            color: 'red',
            fillColor: '#f03',
            fillOpacity: 0.5
            }).addTo(map);
	}
});


