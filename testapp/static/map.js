var map = L.map('map', {
        center: L.latLng(56.834, -3.994),
        zoom: 6,
        minZoom: 5
        });
map.setMaxBounds(L.latLngBounds(L.latLng(50.0,-20.0),L.latLng(65.0,15.0)));

// add an OpenStreetMap tile layer
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);



function buttonClicked(num) {
    switch(num){
        case 0:

            break;
        case 1:

            break;
        case 2:

            break;
        case 3:

            break;
        case 4:

            break;
        case 5:

            break;
        case 6:

            break;
        case 7:

            break;
    }
}

var request_data =  "{\"result\": [    {      \"surname\": \" Scott\",\"percentage_of_interventions_with_mention\": \"0.14208\",      \"total_mentions_of_constituency\": \"723\",\"words\": \"[[\\\"draft\\\",0.465356], [\\\"swinney\\\",0.454288], [\\\"finance\\\",0.421423], [\\\"order\\\",0.351362], [\\\"local\\\",0.302168], [\\\"item\\\",0.260115], [\\\"motion\\\",0.247806], [\\\"business\\\",0.235882]]\",\"mentions_percentage_of_total_text\": \"0.00322376\",\"shit\": 1,      \"avg_intervention_len\": \"133.768\",      \"name\": \"John\",      \"rank_c\": \"53.956609546201\",      \"interventions_with_mention\": \"236\",      \"MSP_id\": \"14091\",      \"url\": \"http://www.scottish.parliament.uk/images/MSPs and office holders Session 4/JohnScottMSP20110509.JPG\",      \"total_interventions\": \"1661\",      \"party\": \"Scottish Conservative and Unionist Party\"    }  ]}";


var geojson = L.geoJson(constituencies, {
    style: style,
    onEachFeature: onEachFeature
}).addTo(map);


// control that shows state info on hover
var InfoControl = L.Control.extend({

    options: {
        position: 'bottomleft'
    },

    onAdd: function (map) {
        this._div = L.DomUtil.create('div', 'info');
        this.update();
        return this._div;
    },

    update: function (results, constituency) {
        if (results) {
        sel_constituency = JSON.parse(results);

        this._div.innerHTML =

        "<h4>"+constituency+"</h4>" +
        "<br/>" +
        "<img src=\"" + sel_constituency.result[0].url.replace(' ','%20') + "\"/>";
        } else {
         this._div.innerHTML = "";
        }
    }
});

var info = new InfoControl();

map.addControl(info);

//Default colour
var defaultColour = '#507FFF';

// get color depending on percentage value
function getColor(d) {
    return d > 90  ? '#FF00FF' :
           d > 80  ? '#FF1CE3' :
           d > 70  ? '#FF38C7' :
           d > 60  ? '#FF55AA' :
           d > 50  ? '#FF718E' :
           d > 40  ? '#FF8D72' :
           d > 30  ? '#FFAA55' :
           d > 20  ? '#FFC639' :
           d > 10  ? '#FFE21D' :
                     '#FFFF00';
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
    info.update(request_data, constituency); //test purposes

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

