d3.csv(".\\data\\data.csv", function(d) {
  var format = d3.time.format("%Y");
  	return {
  		'year': format.parse(d.year),
        'carrier_name': d.carrier_name,
        'on_time': +d.on_time,
        'arrivals': +d.arrivals
  };
}, function(data) {
		'use strict';

        var margin = 80,
            width = 880 - margin,
            height = 560 - margin;

        d3.select('body')
            .append('h2')
            .text('Performance of 6 Largest U.S. Domestic Carriers from 2003 to 2016');
        /*d3.select('#content')
          .append('h2')
          .attr('id', 'title')
          .text('Top U.S. Domestic Airline Performance, 2003-2014');*/

        
        function createSVG() {
            return d3.select("body")
            .append("svg")
              .attr("width", width + margin)
              .attr("height", height + margin)
            .append('g')
                .attr('class','chart');
          };
        function addText(svg, chart, text1) {
            svg.append("text")
           .attr("x", chart._xPixels() + chart._widthPixels() / 2)
           .attr("y", chart._yPixels() - 20)
           .style("text-anchor", "middle")
           .style("font-family", "sans-serif")
           .style("font-weight", "bold")
           .text(text1);

          };  

        var minOnTimeValue = (function(data, field) {
          var minimum = 1;
          data.forEach(function(record) {
            if (record[field] < minimum) {
              minimum = record[field];
            }
          });
          return minimum;
        })(data, 'on_time');
        var minY = Math.round(minOnTimeValue*10)/10,
            maxY = 1;


        //var svg = dimple.newSvg('#content', 960, 640);
        var svg1 = createSVG()
        var Chart1 = new dimple.chart(svg1, data);
        // set x axis
        var x = Chart1.addTimeAxis('x', 'year');
        x.tickFormat = '%Y';
        x.title = 'Year';
        // set y axis
        var y = Chart1.addMeasureAxis('y', 'on_time');
        y.tickFormat = '%Y';
        y.overrideMin = minY;
        y.overrideMax = maxY;
        y.title = 'Percentage of Arrivals on Time (within 15 minutes)';
        addText(svg1, Chart1, "Average Arrivals on Time");
        Chart1.addSeries('carrier_name', dimple.plot.line);
        Chart1.addSeries('carrier_name', dimple.plot.scatter);
        Chart1.addLegend(width*0.65, 60, width*0.25, 60, 'right');
        Chart1.draw();
}
);
