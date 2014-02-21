// var MyCustomLayer = L.Class.extend({

//     initialize: function (latlng) {
//         // save position of the layer or any options from the constructor
//         this._latlng = latlng;
//     },

//     onAdd: function (map) {
//         this._map = map;

//         // create a DOM element and put it into one of the map panes
//         this._el = L.DomUtil.create('div', 'my-custom-layer leaflet-zoom-hide');
//         map.getPanes().overlayPane.appendChild(this._el);

//         // add a viewreset event listener for updating layer's position, do the latter
//         map.on('viewreset', this._reset, this);
//         this._reset();
//     },

//     onRemove: function (map) {
//         // remove layer's DOM elements and listeners
//         map.getPanes().overlayPane.removeChild(this._el);
//         map.off('viewreset', this._reset, this);
//     },

//     _reset: function () {
//         // update layer's position 
//         var pos = this._map.latLngToLayerPoint(this._latlng);
//         L.DomUtil.setPosition(this._el, pos);
//     }
// });

// layer=map.addLayer(new MyCustomLayer(latlng));

var canvasTiles = L.tileLayer.canvas(/*{"tileSize":2000}*/);
// console.log("wordcloud.js");

canvasTiles.drawTile = function(canvas, tilePoint, zoom) {
    var ctx = canvas.getContext('2d');
    ctx.font = "20pt Arial";
    ctx.fillText("Sample String", 10, 50);
   // console.log("painted");
    // draw something on the tile canvas

}

map.addLayer(canvasTiles);

// Load the words for al MSPs
$.getJSON( "msps_words.json", function( data ) {
    var items = [];

    for(i=0;i<data[0].top_words.length;i++){
    // $.each( data[0].top_words, function(  value ) {
      // tuple[1] = tuple[1] * 10000;
      data[0].top_words[i][1] = (data[0].top_words[i][1] * 90) + 12;
    // });
    };

    // console.log(data);

// Paint the word cloud
  var fill = d3.scale.category20();

  d3.layout.cloud().size([500, 500])
      .words(
        data[0].top_words.map(function(d){return {text: d[0], size: d[1]};}))
        // [
        // "Hello", "world", "normally", "you", "want", "more", "words",
        // "than", "this"].map(function(d) {
        // return {text: d, size: 10 + Math.random() * 90};})
        // )
      .padding(5)
      .rotate(function() { return 0 /*~~(Math.random() * 2) * 90;*/ })
      .font("Impact")
      .fontSize(function(d) { return d.size; })
      .on("end", draw)
      .start();

  function draw(words) {
    d3.select("body").append("svg")
        .attr("width", 500)
        .attr("height", 500)
      .append("g")
        .attr("transform", "translate(150,150)")
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


      });
