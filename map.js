

// create a map in the "map" div, set the view to a given place and zoom
var map = L.map('map').setView([56.834, -3.994], 7);

// add an OpenStreetMap tile layer
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var constituencies = new Array();

$.getJSON("./data/constituencies_polygons.js", function (data) {
	constituencies = data;
});

//var polygons = new Array();

//for(int i = 0; i<constituencies.length(); i++) {
//	polygons[i] = L.polygon(constituencies.polygon)).addTo(map);
	//alert(constituencies.name);
//}
