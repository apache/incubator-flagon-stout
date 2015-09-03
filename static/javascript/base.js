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
	var $this = $(this).parents(".expTray");
	$(this).parent().find(".expTrayNavBtn").removeClass("active");
	$(this).addClass("active");
	var id = $(this).attr("id");
	var labelId = id.replace("Btn", "Label");
	$this.find(".expTrayNavBtnLabel").removeClass("active");
	$this.find("#" + labelId).addClass("active");
	var divId = id.slice(0, -3);
	$this.find(".expTraySection").removeClass("active");
	$this.find("#" + divId).addClass("active");
})

$(".metricsNavBtn").click(function(){
	$(this).parent().find(".metricsNavBtn").removeClass("active");
	$(this).addClass("active");
	$(".metricsSection").removeClass("active");
	var id = $(this).attr("id");
	id = id.slice(0, -3);
	$("#" + id).addClass("active");
})

$(".expShelf").click(function(){
	var $thisTray = $(this).parents(".experimentStatusRow").find(".expTray");
	if ($(this).hasClass("active")) {
		$thisTray.fadeOut(300);
		$(this).parents(".experimentStatusRow").animate({"height": "100px"}, 300);
	} else {
		$(this).parents(".experimentStatusRow").animate({"height": "600px"}, 300, function(){
			$thisTray.fadeIn(400);
		})
	}
	$(this).toggleClass("active");
})

var start = true;

loopCharts(start);

$("#toolsSelect, #tasksSelect").change(function(){
	start = false;
	var id = $(this).parents(".experimentStatusRow").attr("id");
	loopCharts(start, id);
})

function loopCharts(start, id) {
	if (start==true) {
		chartsToLoad = ".chart";
	} else {
		chartsToLoad = "#" + id + " .chart";
	}
	$(chartsToLoad).each(function(){
		var chartId = $(this).attr("id");
		var range;
		var metric;

		$(".metricsNavBtn").each(function(){
			if ($(this).hasClass("active")) {
				var id = $(this).attr("id");
				metric = id.replace("Btn", "");
			}
		})

		var tool = $(this).parents(".metricsBody").find("#toolsSelect").val();

		if (tool == "All") {
			tool = "";
		};

		var task = $(this).parents(".metricsBody").find("#tasksSelect").val();

		if (task == "all") {
			task = "";
		} else if (task == "Test-OT1") {
			task = "OT1"
		} else if (task == "Test-OT2") {
			task = "OT2"
		};

		console.log("metric = " + metric);
		console.log("tool = " + tool);
		console.log("task = " + task);

		switch (chartId) {
			case "loadChart":
				dataPath = "load" + task + ".csv"
				break;
			case "difficultyChart":
				dataPath = "difficulty" + task + ".csv"
				break;
			case "performanceChart":
				dataPath = "performance" + task + ".csv"
				break;
			case "confidenceChart":
				dataPath = "confidence" + task + ".csv"
				break;
			case "activityChart":
				dataPath = "activity" + task + ".csv"
				break;
			case "timeChart":
				dataPath = "time" + task + ".csv"
				break;
		}
		$(this).empty();
		buildChart(dataPath, chartId, tool)
	})
}

function buildChart(dataPath, chartId, tool) {
	var margin = {top: 20, right: 30, bottom: 30, left: 40},
	    width = 535 - margin.left - margin.right,
	    height = 350 - margin.top - margin.bottom;

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
	    .ticks(5);

	var chart = d3.select("#" + chartId)
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	d3.csv("/static/javascript/data/" + dataPath, type, function(error, data) {
		
		if (tool !== "all") {
			data = data.filter(function(row) {
				return row["Tool"] == tool;
			});
		};

	  x.domain(data.map(function(d) { return d.Range; }));
	  y.domain([0, d3.max(data, function(d) { return d.Count; })]);

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
	      .attr("x", function(d) { return x(d.Range); })
	      .attr("y", function(d) { return y(d.Count); })
	      .attr("height", function(d) { return height - y(d.Count); })
	      .attr("width", x.rangeBand());
	});

	function type(d) {
	  d.Count = +d.Count; // coerce to number
	  return d;
	}
}

