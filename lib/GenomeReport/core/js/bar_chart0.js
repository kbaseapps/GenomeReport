// javascript
var width = 420,
    barHeight = 20;

var xScale = d3.scaleLinear()
    .range([0, width]);

var chart = d3.select("#chart1")
    .attr("width", width)

d3.tsv("https://gist.githubusercontent.com/qzzhang/4a65cfae97692a7b068ec1bf0ec98c68/raw/7086e9ad31c92ff478ac8bfde8e52ddac3c894eb/data.tsv", type)
  .then(function(data, error) {
    if (error) {
        return console.warn(error);
    }
    console.log(data);
    maxV = d3.max(data, function(d){return d.value});
    xScale.domain([0, d3.max(data, function(d) { return d.value; })]);
    
    chart.attr("height", barHeight * data.length);
    
    var bar = chart.selectAll("g")
        .data(data)
        .enter().append("g")
        .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; });
    
    bar.append("rect")
        .attr("width", function(d) { return xScale(d.value); })
        .attr("height", barHeight - 1);
    
    bar.append("text")
        .attr("x", function(d) { return xScale(d.value) - 3; })
        .attr("y", barHeight / 2)
        .attr("dy", ".35em")
        .text(function(d) { return d.value; });
    });

function type(d) {
    d.value = +d.value; // coerce to number
    return d;
}
