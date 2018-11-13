var search_results = new Vue({
  el: '#search_results',
  mounted: function(){
    draw_graph(get_graph());
  },
  data: {
    results: get_results(),
    nb_datasets: get_nb_datasets(),
    show_sets: false,
    classification: get_classification()
  },
  methods: {
    export_link: function (format) {
      return "../api/" + this.classification + "/exports/" + format;
    }
  }
});

function draw_graph(graph) {
  var svg = d3.select("svg"),
  width = svg.attr("width"),
  height = svg.attr("height");

  var color = d3.scaleOrdinal(d3.schemeCategory10);

  var forceLink = d3
    .forceLink().id(function (d) {
        return  d.node_id;
    })
    .distance(function (d) {
      return (d.value == 1) ? 100 : 40;;
    })
    .strength(1)
    .iterations(10);

  var simulation = d3.forceSimulation()
      .force("link", forceLink)
      .force("charge", d3.forceManyBody().strength(-90))
      .force("center", d3.forceCenter())
      .force('collision', d3.forceCollide().radius(function(d) {return d.radius}));

  svg.append("defs").selectAll("marker")
    .data(["end"])      // Different link/path types can be defined here
  .enter().append("svg:marker")    // This section adds in the arrows
    .attr("id", String)
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 20)
    .attr("refY", 0)
    .attr("markerWidth", 4)
    .attr("markerHeight", 4)
    .attr("orient", "auto")
    .attr("fill", "#999")
  .append("path")
    .attr("d", "M0,-5L10,0L0,5");

  var link = svg.append("g")
      .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
      .attr("stroke-width", function(d) { return (d.value == 1) ? 5 : 2; })
      .attr("marker-end", function(d) { return (d.value == 1) ? "url(#end)" : ""; });

  var node = svg.append("g")
      .attr("class", "nodes")
    .selectAll("circle")
    .data(graph.nodes)
    .enter().append("circle")
      .attr("r", function(d) { return (d.group == 1) ? 20 : 8; })
      .attr("fill", function(d) { return color(d.group); })
      .attr("opacity", function(d) { return (d.group == 1) ? 1 : 0.7; })
      .on("mouseover", mouseover)
      .on("mouseout", mouseout)
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

  node.append("title")
      .text(function(d) { return d.node_label; });

  var node_label = svg.append("g")
    .attr("class", "nodelabels")
    .selectAll("text")
    .data(graph.nodes)
    .enter().append("text")
      .text(function (d) {return d.node_label})
      .style("opacity", function(d) { return (d.group == 1) ? 0.75 : 0; })
      .attr("pointer-events", "none")
      .attr("class", "noselect");

  simulation
      .nodes(graph.nodes)
      .on("tick", ticked)
      .force("link").links(graph.links);



  function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .each(function(d) {d.y -= ((d.level-3)*1.1)})
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

    node_label
        .attr("dx", function(d) { return d.x + 20; })
        .attr("dy", function(d) { return d.y + 10; });
    simulation.alphaTarget(0.3).restart();
  }

  function mouseover() {
  d3.select(this).transition()
      .duration(400)
      .attr("r", function(d) { return (d.group == 1) ? 30 : 12; });
  }

  function mouseout() {
    d3.select(this).transition()
        .duration(400)
        .attr("r", function(d) { return (d.group == 1) ? 20 : 8; });
  }

  function dragstarted(d) {
    //if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }

  function dragended(d) {
    d.fx = null;
    d.fy = null;
  }

  var zoomed = function() {
    link.attr("transform", d3.event.transform);
    node.attr("transform", d3.event.transform);
    node_label.attr("transform", d3.event.transform);
  }

  svg.call(d3.zoom()
  	.scaleExtent([1 / 2, 12])
  	.on("zoom", zoomed));
}

function checkOffset() {
    if($('#graph').offset().top + $('#graph').height()
                                           >= $('#footer').offset().top - 40)
        $('#graph').css('position', 'absolute').css('top', $('#footer').offset().top - $('#graph').height() - 40);
    if($(document).scrollTop() + window.innerHeight < $('#footer').offset().top)
        $('#graph').css('position', 'fixed').css('top', ''); // restore when you scroll up
}
$(document).scroll(function() {
    checkOffset();
});
