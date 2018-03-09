var graph = new Vue({
  el: '#graph',
  data: {
  },
  mounted: function(){
    this.get_graph();
  },
  methods: {
    get_graph: function () {
      this.$http.get('/api/licenses/graph/').then(response => {
        return response.body;
      }).then(json_graph => {
        draw_graph(json_graph);
      });
    },
  },
});

function draw_graph(graph) {
  var svg = d3.select("svg"),
  width = +svg.attr("width"),
  height = +svg.attr("height");

  var color = d3.scaleOrdinal(d3.schemeCategory10);

  var forceLink = d3
    .forceLink().id(function (d) {
        return  d.node_id;
    })
    .distance(function (d) {
      return (d.value == 1) ? 130 : 50;;
    })
    .strength(1);

  var simulation = d3.forceSimulation()
      .force("link", forceLink)
      .force("charge", d3.forceManyBody().strength(-100))
      .force("center", d3.forceCenter(width, height))
      .force('collision', d3.forceCollide().radius(function(d) {return d.radius}));

  svg.append("defs").selectAll("marker")
    .data(["end"])      // Different link/path types can be defined here
  .enter().append("svg:marker")    // This section adds in the arrows
    .attr("id", String)
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 21)
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
      .text(function (d) {return (d.group == 1) ? d.node_label : ""; })
      .attr("pointer-events", "none");

  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

  simulation.force("link")
      .links(graph.links);

  function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

    node_label
        .attr("dx", function(d) { return d.x + 20; })
        .attr("dy", function(d) { return d.y + 10; });
  }

  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }

  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }
}

var chart = $("#chart"),
    aspect = chart.width() / chart.height(),
    container = chart.parent();
$(window).on("resize", function() {
    var targetWidth = container.width();
    chart.attr("width", targetWidth);
    chart.attr("height", Math.round(targetWidth / aspect));
}).trigger("resize");
