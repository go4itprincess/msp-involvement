var map = L.map('map', {
        center: L.latLng(56.834, -3.994),
        zoom: 7,
        minZoom: 5
        });
map.setMaxBounds(L.latLngBounds(L.latLng(50.0,-20.0),L.latLng(65.0,15.0)));

// add an OpenStreetMap tile layer
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var constituencies = [];
var polygons = [];

$.getJSON("constituencies_polygons.js", function (data) {
	constituencies = data;
	console.log(constituencies[0].polygon);
	for(var i = 0; i<Object.keys(constituencies).length; i++){
		polygons[i] = L.multiPolygon(constituencies[i].polygon).addTo(map);
		polygons[i].bindPopup("<b>" + constituencies[i].name + "</b>")
	}
});


