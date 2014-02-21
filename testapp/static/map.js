var flag = 'rank_gen';

$(".button-top").on('click', function(e) {
    e.stopPropagation();
    var element = $(e.currentTarget);
    $(".button-top-selected").removeClass("button-top-selected");
    element.addClass("button-top-selected");
    flag = element.attr('id');
    map.removeLayer(geojson);
    geojson = L.geoJson(constituencies, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(map);

});

var percentColors = [
    { pct: 0.0, color: { r: 0xff, g: 0x00, b: 0 } },
    { pct: 0.5, color: { r: 0xff, g: 0xff, b: 0 } },
    { pct: 1.0, color: { r: 0x00, g: 0xff, b: 0 } } ];

var getColorForPercentage = function(pct) {
    for (var i = 1; i < percentColors.length - 1; i++) {
        if (pct < percentColors[i].pct) {
            break;
        }
    }
    var lower = percentColors[i - 1];
    var upper = percentColors[i];
    var range = upper.pct - lower.pct;
    var rangePct = (pct - lower.pct) / range;
    var pctLower = 1 - rangePct;
    var pctUpper = rangePct;
    var color = {
        r: Math.floor(lower.color.r * pctLower + upper.color.r * pctUpper),
        g: Math.floor(lower.color.g * pctLower + upper.color.g * pctUpper),
        b: Math.floor(lower.color.b * pctLower + upper.color.b * pctUpper)
    };
    return 'rgb(' + [color.r, color.g, color.b].join(',') + ')';
    // or output as hex if preferred
};

var map = L.map('map', {
        center: L.latLng(56.834, -3.994),
        zoom: 6,
        minZoom: 5
        });

map.setMaxBounds(L.latLngBounds(L.latLng(50.0,-20.0),L.latLng(65.0,15.0)));

// add an OpenStreetMap tile layer
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {attribution: ' Data from: <a href="http://www.theyworkforyou.com/">TheyWorkForYou</a>, <a href="http://www.sns.gov.uk/">SNS</a> and <a href="http://mapit.mysociety.org/">MapIt</a> | &copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);


var request_data =  "{\"result\": [    {      \"surname\": \" Scott\",\"percentage_of_interventions_with_mention\": \"0.14208\",      \"total_mentions_of_constituency\": \"723\",\"words\": \"[[\\\"draft\\\",0.465356], [\\\"swinney\\\",0.454288],[\\\"finance\\\",0.421423], [\\\"order\\\",0.351362], [\\\"local\\\",0.302168], [\\\"item\\\",0.260115], [\\\"finance\\\",0.421423], [\\\"order\\\",0.351362], [\\\"local\\\",0.302168], [\\\"item\\\",0.260115], [\\\"motion\\\",0.247806], [\\\"business\\\",0.235882]]\",\"mentions_percentage_of_total_text\": \"0.00322376\",\"shit\": 1,      \"avg_intervention_len\": \"133.768\",      \"name\": \"John\",      \"rank_c\": \"53.956609546201\",      \"interventions_with_mention\": \"236\",      \"MSP_id\": \"14091\",      \"url\": \"http://www.scottish.parliament.uk/images/MSPs and office holders Session 4/JohnScottMSP20110509.JPG\",      \"total_interventions\": \"1661\",      \"party\": \"Scottish Conservative and Unionist Party\"    }  ]}";


var geojson = L.geoJson(constituencies, {
    style: style,
    onEachFeature: onEachFeature
}).addTo(map);

 var fill = d3.scale.category20();
 var tagXsize=400;
 var tagYsize=200;
 var drawTagCloudOn=0;
 var currentArea=0;  // Stores the area that we most recently hovered over
window.currentData=0;  // Stores the area that we most recently hovered over
 var currentConstituency=0; // Stores the name of the constituency that we most recently hovered over

 
  function draw(words) {
    // d3.select("body").append("svg")
    // console.log("drawing");
    // d3.select(map.getPanes().overlayPane).append("svg")
    d3.select(drawTagCloudOn).select("svg")
    // d3.select(".info").append("svg")
        .attr("width", tagXsize)
        .attr("height", tagYsize)
        // .attr("align","left")
        // .attr("valign","bottom")
      .append("g")
        .attr("transform", "translate("+tagXsize/2+","+tagYsize/2+")")
      .selectAll("text")
        .data(words)
      .enter().append("text")
        .style("font-size", function(d) { return d.size + "px"; })
        .style("font-family", "Impact")
        .style("fill", function(d, i) { return fill(i); })
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {
          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) { return d.text; });
  }


function htmlForMSP(data,region) {
    // <span style='padding-left:12px;'>
        res="<span class='mspname'> MSP "+data.name+" "+data.surname+"</span>"+
        "<span class='infotext'>("+region+")</span>"+
        "<span class='infotext'> Total interventions: "+data.total_interventions+"</span>"+
        "<span class='infotext'> Average words spoken: "+data.avg_intervention_len+"</span>"+
        // "<span class='infotext'> total_mentions_of_constituency: "+data.total_mentions_of_constituency+"</span>"+
        "<span class='infotext'> Interventions about constituency: "+data.interventions_with_mention+"</span>"+
        "<img src=\"" + data.url.replace(' ','%20') + "\"/>"+
        "<svg > </svg>" ;
        return res;
}

function paintTagCloud(element, words) {
        drawTagCloudOn=element;
        d3.layout.cloud().size([tagXsize, tagYsize])
          .words(
            words.map(function(d){return {text: d[0], size: (d[1]*60)+8};}))
          .padding(5)
          .rotate(function() { return 0/*~~(Math.random() * 2) * 90*/;})
          .font("Impact")
          .fontSize(function(d) { return d.size; })
          .on("end", draw)
          .start();
}


function paintLightBox() {
    // this.inner.prepend( '<h1>1. My custom title</h1>' );
    // this.content = '<h1>2. My custom title</h1>' + this.content.html();

    window.lightbox=this;

    $.ajax({
        url:"/region/" + constituency,
        // url:"/example.json",
        success: function(result) {
            // console.log(result);
            data=result.result;
            // console.log(data);
            content="<div class='constdiv'>"+ barHTML(window.currentData.result[0], window.currentData.result[0].region)+
            "</div>";

            content+="<div class='mpsdiv'>"

            content=content+
            "<div id=msp1 class='persondiv'>"+
            htmlForMSP(window.currentData.result[0],window.currentData.result[0].party+", "+currentConstituency) +
            "</div>";

            for (cnt=0; cnt < data.length; cnt++){
                content=content+
                "<div id=msp"+(cnt+2)+"  class='persondiv'>"+
                htmlForMSP(data[cnt],data[cnt].party+", "+data[cnt].region) +
                "</div>";
            }
            content+="</div>";

            window.lightbox.inner.append(content);

            words=JSON.parse(window.currentData.result[0].words);
            paintTagCloud("#msp1", words);

            // console.log(data);
            for (cnt=0;cnt < data.length; cnt++){
                // words=data[cnt].words;
                words=JSON.parse(data[cnt].words);
                paintTagCloud("#msp"+(cnt+2), words);
            }

            $(window).bind('resize', function() {
            var top = ($(window).height() / 2) - ($(".fancybox-wrap").outerHeight() / 2);
            var left = ($(window).width() / 2) - ($(".fancybox-wrap").outerWidth() / 2);
            $(".fancybox-wrap").css({ top: top, left: left});
            var height=$(".fancybox-wrap").outerHeight()-20;
            // console.log(height);
            $(".mpsdiv").css({"height": height});
        }).trigger('resize');

        },
        error: function() {
            this.innerHTML="ERROR LOADING";
        }
    });


}


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
        sel_constituency = results;


        words=JSON.parse(sel_constituency.result[0].words);

        this._div.innerHTML =
        "<div id=msp1><h4>"+constituency+"</h4>" +
        htmlForMSP(sel_constituency.result[0],sel_constituency.result[0].party) +
        "</div>";
        paintTagCloud("#msp1", words);

        } else {
         this._div.innerHTML = "<p>Hover over a constituency.</p>";
        }

    }
});

var info = new InfoControl();

map.addControl(info);

function style(feature) {
    return {
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7,
        fillColor: getColorForPercentage(feature.properties.ranks[flag]/100)
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
    constituency = layer.feature.properties.name;

    $(e.target).attr('href', '#inline1');
    currentArea=e.target;
    currentConstituency=constituency;

    $(e.target).fancybox({
                    // wrapCSS    : 'fancybox-custom',
                    closeClick : true,

                    openEffect : 'elastic',
                    closeEffect: 'elastic',
                    autoSize: false,
                    width: "970px",
                    height: "500px",
                    scrolling: "no",

                    afterLoad   : paintLightBox,
                    helpers : {
                    title : {
                        type : 'inside'
                    },
                    overlay : {
                        css : {
                            'background' : 'rgba(238,238,238,0.65)'
                        }
                    }
                }

                });


    $.ajax({
        // url:"/example2.json",
        url:"/constituency/" + constituency,
        success: function(result) {
            // console.log(result);
//            result=JSON.parse(result);
            info.update(result, constituency);
            window.currentData=result;

        },
        error: function() {
            // console.log("ERROR LOADING CONSTITUENCY DATA");
            // info.update(request_data, constituency); //test purposes
        }
    });
}

function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();
}

function onClick(e) {
    map.fitBounds(e.target.getBounds());
    highlightFeature(e);
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight
        // click: onClick
    });
}

// control that shows state info on hover
var legendPanel = L.Control.extend({

    options: {
        position: 'bottomright'
    },

    onAdd: function (map) {
        this._div = L.DomUtil.create('div', 'legend');
        this._div.innerHTML =
            "<div id=\"gradient\"></div>" +
            "<div id=\"legendMaxMin\">" +
            "<p id=\"max\">Max</p>" +
            "<p id=\"min\">Min</p>" +
            "</div>"
        return this._div;
    }
});

var legend = new legendPanel();

map.addControl(legend);



var barWidth = 200;

var bar = function(num) {
    return '<div style="float:right; width:' + barWidth + 'px; height:15px;"><div style="opacity:0.9; background-color:' + getColorForPercentage(num/100) + '; height:15px; width:' + Math.floor(barWidth*num/100) + 'px; box-shadow: 0 0 15px rgba(0,0,0,0.2); border-radius: 5px;"></div></div>'
}

function barHTML(data,region){

res ="<span class='infotitle'>" + currentConstituency + " </span>" +
    "<span class='bartext'>(Region of " + region + ")</span><br/><br/>" +
    '<div class="bar-containers">' +
        '<span class="bartext">Population</span>' + '<div style="float:right; width:' + barWidth + 
        'px; height:15px;"><div class=infotext style="float:left;">' + data.population+ '</div></div>' +
    '</div>' + 
    '<div class="bar-containers">' +
        '<span class="bartext">Overall</span>' + bar(data.rank_gen) +
    '</div>' + 
    '<div class="bar-containers">' +
        '<span class="bartext">Crime</span>' + bar(data.rank_cri) +
    '</div>' + 
    '<div class="bar-containers">' +
        '<span class="bartext">Access</span>' + bar(data.rank_geo) +
    '</div>' + 
    '<div class="bar-containers">' +
        '<span class="bartext">Housing</span>' + bar(data.rank_hou) +
    '</div>' + 
    '<div class="bar-containers">' +
        '<span class="bartext">Education</span>' + bar(data.rank_edu) +
    '</div>' + 
    '<div class="bar-containers">' +
        '<span class="bartext">Health</span>' + bar(data.rank_hea) +
    '</div>' + 
    '<div class="bar-containers">' +
        '<span class="bartext">Employement</span>' + bar(data.rank_emp) +
    '</div>' + 
    '<div class="bar-containers">' +
        '<span class="bartext">Income</span>' + bar(data.rank_inc) +
    '</div>';

    return res;
}
