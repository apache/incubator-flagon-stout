$(".expTrayNavBtn").hover(function(){
	var id = $(this).attr("id");
	id = id.replace("Btn", "Label");
	$(".expTrayNavBtnLabel").hide();
	$("#" + id).show();
	// var labelWidth = parseInt($(this).find(".expTrayNavBtnLabel").css("width"));
	// var btnWidth = parseInt($(this).css("width"));
	// var newWidth = labelWidth + btnWidth + 18;
	// $(this).css("width", newWidth + "px");
}, function(){
	$(".expTrayNavBtnLabel").hide();
	$(".expTrayNavBtnLabel").each(function(){
		if ($(this).hasClass("active")) {
			$(this).show();
		}
	});
	// $(this).css("width", "60px");
	// $(this).find(".expTrayNavBtnLabel").hide();
})

$(".expTrayNavBtn").on("click", function(){
	$(this).parent().find(".expTrayNavBtn").removeClass("active");
	$(this).addClass("active");
	var id = $(this).attr("id");
	id = id.replace("Btn", "Label");
	$(".expTrayNavBtnLabel").removeClass("active");
	$("#" + id).addClass("active");
})

$(".metricsNavBtn").click(function(){
	$(this).parent().find(".metricsNavBtn").removeClass("active");
	$(this).addClass("active");
	$(".metricsSection").removeClass("active");
	var id = $(this).attr("id");
	id = id.slice(0, -3);
	$("#" + id).addClass("active");
})

$(".chart").each(function(){
	var chartId = $(this).attr("id");
	var dataPath = "";

	switch (chartId) {
		case "loadChart":
			dataPath = "loadData.tsv"
			buildChart(dataPath, chartId)
			break;
		case "difficultyChart":
			dataPath = "difficultyData.tsv"
			buildChart(dataPath, chartId)
			break;
		case "performanceChart":
			dataPath = "performanceData.tsv"
			buildChart(dataPath, chartId)
			break;
		case "confidenceChart":
			dataPath = "confidenceData.tsv"
			buildChart(dataPath, chartId)
			break;
		case "activityChart":
			dataPath = "activityData.tsv"
			buildChart(dataPath, chartId)
			break;
		case "timeChart":
			dataPath = "timeData.tsv"
			buildChart(dataPath, chartId)
			break;
	}
})

function buildChart(dataPath, chartId) {
	var margin = {top: 20, right: 30, bottom: 30, left: 40},
	    width = 600 - margin.left - margin.right,
	    height = 392 - margin.top - margin.bottom;

	var x = d3.scale.ordinal()
	    .rangeRoundBands([0, width], .1);

	var y = d3.scale.linear()
	    .range([height, 0]);

	var xAxis = d3.svg.axis()
	    .scale(x)
	    .orient("bottom")

	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient("left")
	    .ticks(10, "%");

	var chart = d3.select("#" + chartId)
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	d3.tsv("/static/javascript/fakeData/" + dataPath, type, function(error, data) {
	  x.domain(data.map(function(d) { return d.letter; }));
	  y.domain([0, d3.max(data, function(d) { return d.frequency; })]);

	  chart.append("g")
	      .attr("class", "x axis")
	      .attr("transform", "translate(0," + height + ")")
	      .call(xAxis);

	  chart.append("g")
	      .attr("class", "y axis")
	      .call(yAxis)
	    .append("text")
		    .attr("transform", "rotate(-90)")
		    .attr("y", 6)
		    .attr("dy", ".71em")
		    .style("text-anchor", "end")
		    .text("Frequency");

	  chart.selectAll(".bar")
	      .data(data)
	    .enter().append("rect")
	      .attr("class", "bar")
	      .attr("x", function(d) { return x(d.letter); })
	      .attr("y", function(d) { return y(d.frequency); })
	      .attr("height", function(d) { return height - y(d.frequency); })
	      .attr("width", x.rangeBand());
	});

	function type(d) {
	  d.frequency = +d.frequency; // coerce to number
	  return d;
	}
}

