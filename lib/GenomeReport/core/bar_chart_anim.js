// javascript
var dataset = [
  {"name": "CDS", "value": 460}, 
  {"name": "gene", "value": 493},
  {"name": "ncRNA", "value": 10},
  {"name": "protein_encoding_gene", "value": 460},
  {"name": "rRNA", "value": 6},
  {"name": "non-protein_encoding_gene", "value": 33}, 
  {"name": "tRNA", "value": 26}
]

var margin = {top: 20, right: 30, bottom: 30, left: 40},
    width = 720 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

var xScale = d3.scaleBand()
    .range([margin.left, width - margin.right])
    .padding(0.1);

var yScale = d3.scaleLinear()
    .range([height - margin.bottom, margin.top]);

var xAxis = d3.axisBottom(xScale);

var yAxis = d3.axisLeft(yAxis)
    .tickFormat(function(d){
      return parseInt(d);
    })
    .scale(yScale);

var chart = d3.select("#chart3")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

chart.append("text")
    .attr("transform", "translate(" + (width / 3) + ", -40)")
    .attr("x", 50)
    .attr("y", 50)
    .attr("font-size", "22px")
    .text("Feature counts")

xScale.domain(dataset.map(d => d.name));
yScale.domain([0, d3.max(dataset, d => d.value)]).nice();

chart.append("g")
    .attr("class", "x axis")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(xAxis.tickSizeOuter(0))
    .append("text")
    .attr("y", height / 10)
    .attr("x", width / 2)
    .attr("text-anchor", "end")
    .attr("stroke", "steelblue")
    .text("Features");

chart.append("g")
    .attr("class", "y axis")
    .attr("transform", `translate(${margin.left},0)`)
    .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("x", -height / 2)
      .attr("dx", "3.1em")
      .attr("y", margin.top / 2)
      .attr("dy", "-5.1em")
      .attr("text-anchor", "end")
      .attr("stroke", "steelblue")
      .text("Count");

chart.selectAll(".bar")
      .data(dataset)
    .enter().append("rect")
      .attr("class", "bar")
      .on("mouseover", onMouseOver) //Add listener for the mouseover event
      .on("mouseout", onMouseOut)   //Add listener for the mouseout event
      .attr("x", function(d) { return xScale(d.name); })
      .attr("y", function(d) { return yScale(d.value); })
      .attr("height", function(d) { return height - yScale(d.value) - margin.bottom; })
      .attr("width", xScale.bandwidth)
      .transition()
        .ease(d3.easeLinear)
        .duration(400)
        .delay(function (d, i) {
            return i * 50;
        });
    
//mouseover event handler function
function onMouseOver(d, i) {
  d3.select(this).attr('class', 'highlight');
  d3.select(this)
    .transition()     // adds animation
    .duration(400)
    .attr('width', xScale.bandwidth() + 5)
    .attr("y", function(d) { return yScale(d.value) - 10; })
    .attr("height", function(d) { return height - yScale(d.value) - margin.bottom + 10; });

  chart.append("text")
    .attr('class', 'val') 
    .attr('x', function() {
        return xScale(d.name);
    })
    .attr('y', function() {
        return yScale(d.value) - 15;
    })
    .text(function() {
        return [ d.value ];  // Value of the text
    });
}

//mouseout event handler function
function onMouseOut(d, i) {
  // use the text label class to remove label on mouseout
  d3.select(this).attr('class', 'bar');
  d3.select(this)
    .transition()     // adds animation
    .duration(400)
    .attr('width', xScale.bandwidth())
    .attr("y", function(d) { return yScale(d.value); })
    .attr("height", function(d) { return height - yScale(d.value) - margin.bottom; });

  d3.selectAll('.val')
    .remove()
}
