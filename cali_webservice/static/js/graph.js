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

  var color = d3.scaleOrdinal(d3.schemeCategory20);

  var simulation = d3.forceSimulation()
      .force("link", d3.forceLink().id(function(d) { return d.node_id; }))
      .force("charge", d3.forceManyBody())
      .force("center", d3.forceCenter(width / 2, height / 2));

  var link = svg.append("g")
      .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
      .attr("stroke-width", function(d) { return Math.sqrt(d.value) + 3; });

  var node = svg.append("g")
      .attr("class", "nodes")
    .selectAll("circle")
    .data(graph.nodes)
    .enter().append("circle")
      .attr("r", 15)
      .attr("fill", function(d) { return color(d.group); })
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

  node.append("title")
      .text(function(d) { return d.node_label; });

  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

  simulation.force("link")
      .links(graph.links);

  function ticked() {
    link
        .attr("x1", function(d) { return d.source.x * 2; })
        .attr("y1", function(d) { return d.source.y * 2; })
        .attr("x2", function(d) { return d.target.x * 2; })
        .attr("y2", function(d) { return d.target.y * 2; });

    node
        .attr("cx", function(d) { return d.x * 2; })
        .attr("cy", function(d) { return d.y * 2; });
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
