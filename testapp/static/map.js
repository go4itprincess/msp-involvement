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

var request_data =  "{\"result\": [{\"surname\": \" Gibson\", \"percentage_of_interventions_with_mention\": \"0.00227\", \"total_mentions_of_constituency\": \"3\", \"words\": \"[['uk',0.307912], ['miller',0.234796], ['farming',0.224131], ['support',0.204922], ['cap',0.172721], ['vital',0.160378], ['farm',0.154422], ['funding',0.146016], ['production',0.145559], ['ball',0.128258], ['coupling',0.128258], ['eustice',0.128258], ['gaindykehead',0.128258], ['lever',0.128258], ['nigel',0.128258], ['airdrie',0.121905], ['stunning',0.121905], ['debacle',0.117398], ['hectare',0.113902], ['paterson',0.113902], ['competitors',0.111045], ['convergence',0.111045], ['coupled',0.111045], ['owen',0.111045], ['rough',0.111045], ['defra',0.10863], ['edition',0.10863], ['pressures',0.10863], ['dig',0.106538], ['door',0.106538], ['farmer',0.106538], ['grazing',0.106538], ['burns',0.104693], ['implementation',0.104693], ['leadership',0.104693], ['nfu',0.104693], ['controlled',0.101549], ['played',0.0989313], ['double',0.0966892], ['southern',0.0966892], ['targeted',0.0966892], ['actions',0.095678], ['budgets',0.0929855], ['george',0.0921819], ['remove',0.0899922], ['brown',0.0893253], ['foundation',0.0893]\", \"mentions_percentage_of_total_text\": \"0.00000983539\", \"shit\": 1, \"avg_intervention_len\": \"228.966\", \"name\": \"Rob\", \"rank_c\": \"45.106429904783\", \"interventions_with_mention\": \"3\", \"MSP_id\": \"13993\", \"url\": \"http://www.scottish.parliament.uk/images/MSPs and office holders Session 4/RobGibsonMSP20110510.JPG\", \"total_interventions\": \"1321\", \"party\": \"Scottish National Party\"}]}"

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

        console.log(sel_constituency);

        this._div.innerHTML =  "<b>"+constituency+"</b>"
        ;


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

