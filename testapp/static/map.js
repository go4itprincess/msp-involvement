var map = L.map('map', {
        center: L.latLng(56.834, -3.994),
        zoom: 6,
        minZoom: 5
        });
map.setMaxBounds(L.latLngBounds(L.latLng(50.0,-20.0),L.latLng(65.0,15.0)));

// add an OpenStreetMap tile layer
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

//var constituencies = [];
//var polygons = [];

/*$.getJSON("constituencies_polygons.js", function (data) {
	constituencies = data;
	console.log(constituencies[0].polygon);
	for(var i = 0; i<Object.keys(constituencies).length; i++){
		polygons[i] = L.multiPolygon(constituencies[i].polygon).addTo(map);
		polygons[i].bindPopup("<b>" + constituencies[i].name + "</b>")
	}
});
*/



var geojson = L.geoJson(constituencies, {
    style: style,
    onEachFeature: onEachFeature
}).addTo(map);


// control that shows state info on hover
var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info');
    this.update();
    return this._div;
};

info.update = function (results, constituency) {
    if (results) {this._div.innerHTML =  constituency + results;}
};

info.addTo(map);


// get color depending on percentage value
function getColor(d) {
    return d > 90  ? '#800026' :
           d > 80  ? '#BD0026' :
           d > 70  ? '#E31A1C' :
           d > 60  ? '#FC4E2A' :
           d > 50  ? '#FD8D3C' :
           d > 40  ? '#FEB24C' :
           d > 30  ? '#FED976' :
           d > 20  ? '#FED976' :
           d > 10  ? '#FED976' :
                     '#FFEDA0';
}

function style(feature) {
    return {
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7,
        fillColor: getColor(feature.properties.population/1000)
    };
}

function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera) {
        layer.bringToFront();
    }
    constituency = layer.feature.properties.name
    $.ajax({url:"/constituency/" + constituency, success: function(result) {
        info.update(result, constituency);
        }
    });

}



function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();
}

function onClick(e) {
    map.fitBounds(e.target.getBounds());
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: onClick
    });
}



var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        labels = [],
        from, to;

    for (var i = 0; i < grades.length; i++) {
        from = grades[i];
        to = grades[i + 1];

        labels.push(
            '<i style="background:' + getColor(from + 1) + '"></i> ' +
            from + (to ? '&ndash;' + to : '+'));
    }

    div.innerHTML = labels.join('<br>');
    return div;
};

legend.addTo(map);
