var map = L.map('map').setView([56.834, -3.994], 7);

// add an OpenStreetMap tile layer
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var constituencies = [];
var polygons = [];

$.getJSON("./data/constituencies_polygons.js", function (data) {
	constituencies = data;
	console.log(constituencies[0].polygon);
	for(var i = 0; i<Object.keys(constituencies).length; i++){
		polygons[i] = L.polygon(constituencies[i].polygon).addTo(map);
		console.log(constituencies[i].name);
		console.log(i);
	}
});


