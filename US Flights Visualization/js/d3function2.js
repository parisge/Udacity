d3.csv(".\\data\\data.csv", function(d) {
  var format = d3.time.format("%Y");
  	return {
  		  'year': format.parse(d.year),
        'carrier_name': d.carrier_name,
        'on_time': +d.on_time,
        'arrivals': +d.arrivals,
        'percent_delays': +d.percent_car_delays,
        'average_delays': +d.av_car_delay
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

          function addSeries(series, chart) {
            chart.addSeries("carrier_name", dimple.plot.line);
            chart.addSeries("carrier_name", dimple.plot.scatter);
            chart.assignColor("SkyWest Airlines Inc.", "yellow");
            chart.assignColor("Delta Air Lines Inc.", "red");
            chart.assignColor("Southwest Airlines Co.", "purple");
            chart.assignColor("United Air Lines Inc.", "lightblue");
            chart.assignColor("American Eagle Airlines Inc.", "green");
            chart.assignColor("American Airlines Inc.", "darkblue");
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
            maxY = 0.95;


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
        y.title = 'Percentage of Arrivals on Time ';
        addSeries('carrier_name', Chart1);
        //Chart1.addSeries('carrier_name', dimple.plot.line);
        //Chart1.addSeries('carrier_name', dimple.plot.scatter);
        var legend = Chart1.addLegend(width*0.80, 80, width*0.25, 80, 'right');
        addText(svg1, Chart1, "Average Percent Arrivals on Time");

        Chart1.draw();

        var svg2 = createSVG()
        var Chart2 = new dimple.chart(svg2, data);
        // set x axis
        var x = Chart2.addTimeAxis('x', 'year');
        x.tickFormat = '%Y';
        x.title = 'Year';
        // set y axis
        var y = Chart2.addMeasureAxis('y', 'percent_delays');
        y.tickFormat = '%Y';
        y.title = 'Percentage of Carrier Delays';
        addSeries('carrier_name', Chart2);
        //Chart2.addSeries('carrier_name', dimple.plot.line);
        //Chart2.addSeries('carrier_name', dimple.plot.scatter);
        var legend = Chart2.addLegend(width*0.80, 80, width*0.25, 80, 'right');
        addText(svg2, Chart2, "Percent of Delays attributed to Carrier");

        Chart2.draw();

        var svg3 = createSVG()
        var Chart3 = new dimple.chart(svg3, data);
        // set x axis
        var x = Chart3.addTimeAxis('x', 'year');
        x.tickFormat = '%Y';
        x.title = 'Year';
        // set y axis
        var y = Chart3.addMeasureAxis('y', 'average_delays');
        y.tickFormat = 'Y';
        y.overrideMin = 6
        y.overrideMax = 30
        y.title = 'Time of Carrier Delays (in minutes)';
        addSeries('carrier_name', Chart3);
        //Chart3.addSeries('carrier_name', dimple.plot.line);
        //Chart3.addSeries('carrier_name', dimple.plot.scatter);
        var legend = Chart3.addLegend(width*0.80, 80, width*0.25, 80, 'right');
        addText(svg3, Chart3, "Average Time attributed to Carriers");

        Chart3.draw();

              // handle mouse events on gridlines
        y.gridlineShapes.selectAll('line')
          .style('opacity', 0.25)
          .on('mouseover', function(e) {
            d3.select(this)
              .style('opacity', 1);
          }).on('mouseleave', function(e) {
            d3.select(this)
              .style('opacity', 0.25);
          });

        // handle mouse events on paths
        d3.selectAll('path')
          .style('opacity', 0.25)
          .on('mouseover', function(e) {
            d3.select(this)
              .style('stroke-width', '8px')
              .style('opacity', 1)
              .attr('z-index', '1');
        }).on('mouseleave', function(e) {
            d3.select(this)
              .style('stroke-width', '2px')
              .style('opacity', 0.25)
              .attr('z-index', '0');


}
);
