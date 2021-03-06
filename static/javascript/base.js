var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$("#contacts li").click(function(){
	var emailAddress = $(this).html();
	$("#email-to").val(emailAddress);
})

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

$("#statusMessage").bind("DOMSubtreeModified", function(){
	if ($(this).hasClass("0")) {
		$(this).css("color", "red");
	} else if ($(this).hasClass("1")) {
		$(this).css("color", "red");
	} else {
		$(this).css("color", "#000");
	}
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

	if(divId=="metrics") {
		var experiment = $(this).parents(".experimentStatusRow").attr("id");
		var category = $this.find(".metricsNavBtn.active").attr("data-category");
		var mparams = {"experiment":experiment,"tool":$this.find("#toolsSelect").val(),"task":$this.find("#tasksSelect").val(),"category":category};
		getHistData(experiment, category, JSON.stringify(mparams));
	}
})

$(".metricsNavBtn").click(function(){
	$(this).parent().find(".metricsNavBtn").removeClass("active");
	$(this).addClass("active");
	//var rowId = $(this).parents(".experimentStatusRow").attr("id");
	//$("#" + rowId + " .metricsSection").removeClass("active");
	//var id = $(this).attr("id");
	//id = id.slice(0, -3);
	//$("#" + id).addClass("active");

	var $this = $(this).parents(".expTray");
	var experiment = $(this).parents(".experimentStatusRow").attr("id");
	var category = $(this).attr("data-category");
	var mparams = {"experiment":experiment,"tool":$this.find("#toolsSelect").val(),"task":$this.find("#tasksSelect").val(),"category":category};
	//console.log(".metricsNavBtn experiment = ", mparams);
	getHistData(experiment, category, JSON.stringify(mparams)); 
})

$(".expShelf").click(function(){
	if ($(this).parents(".experimentStatusRow").is(":animated")) return false;
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
//	start = false;
//	var id = $(this).parents(".experimentStatusRow").attr("id");
//	$(".chart").empty();
//	loopCharts(start, id);

        var $this = $(this).parents(".expTray");
        var experiment = $(this).parents(".experimentStatusRow").attr("id");
        var category = $this.find(".metricsNavBtn.active").attr("data-category");
       
	var tasklists = JSON.parse($this.find("#tasklists").attr("data-tasklists"));
 
        if($(this).attr("id")=="toolsSelect") {
		// populate the task select
		var toolName = $(this).val();
		var opStr = '<option value="all" selected>All</option>';
		if(toolName!="all" && tasklists[toolName]) {
			for(var i=0; i<tasklists[toolName].length; i++) {
				opStr += '<option value="'+tasklists[toolName][i]+'">'+tasklists[toolName][i]+'</option>';
			} 
		}
		$this.find("#tasksSelect").html(opStr);
        }

	var mparams = {"experiment":experiment,"tool":$this.find("#toolsSelect").val(),"task":$this.find("#tasksSelect").val(),"category":category};
        //console.log(".metricsNavBtn experiment = ", mparams);
        getHistData(experiment, category, JSON.stringify(mparams));

});

function loopCharts(start, id) {
	if (start==true) {
		//startChartBuildwithToolLists();
		buildCharts();
	} else if (start==false) {
		buildCharts();
	}
}

function startChartBuildwithToolLists() {
	$(".experimentStatusRow").each(function(){
		var expName = $(this).find(".expName").html();
		$.ajax({
			url: "../static/results/" + expName + "/tools.json",
			dataType: "json"
		}).done(function(data){
			var tools = data.Tools;
			for (i in tools) {
				var html = '<option value="' + tools[i] + '">' + tools[i] + '</option>';
				$("#" + expName + " #toolsSelect").append(html);
			}
			buildCharts();
		})
	})
}

function buildCharts(){
	$(".chart").each(function(){
		var chartId = $(this).attr("id");
		var range;
		var metric;

		$(".metricsNavBtn").each(function(){
			if ($(this).hasClass("active")) {
				var id = $(this).attr("id");
				metric = id.replace("Btn", "");
			}
		})

		var expName = $(this).parents(".experimentStatusRow").attr("id");

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

		var dataPath = "";

		// paths are based on location of d3.js file...
		switch (chartId) {
			case expName + "LoadChart":
				dataPath = "../../results/" + expName + "/load" + task + ".csv";
				break;
			case expName + "DifficultyChart":
				dataPath = "../../results/" + expName + "/difficulty" + task + ".csv";
				break;
			case expName + "PerformanceChart":
				dataPath = "../../results/" + expName + "/performance" + task + ".csv";
				break;
			case expName + "ConfidenceChart":
				dataPath = "../../results/" + expName + "/confidence" + task + ".csv";
				break;
			// case expName + "ActivityChart":
			// 	dataPath = "../../results/" + expName + "/activity" + task + ".csv";
			// 	break;
			case expName + "TimeChart":
				dataPath = "../../results/" + expName + "/time" + task + ".csv";
				break;
		}
		// $(this).empty();
		buildD3Chart(dataPath, chartId, tool)
	})
};

function buildD3Chart(dataPath, chartId, tool) {
	var margin = {top: 20, right: 30, bottom: 40, left: 50},
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
	      .call(xAxis)
	    .append("text")
		    .attr("y", 25)
		    .attr("x", 230)
		    .attr("dy", "1em")
		    .style("text-anchor", "end")
		    .text("Value");

	  chart.append("g")
	      .attr("class", "y axis")
	      .call(yAxis)
	    .append("text")
		    .attr("transform", "rotate(-90)")
		    .attr("y", -50)
		    .attr("dy", "1em")
		    .style("text-anchor", "end")
		    .text("Count");

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

function getHistData(experimentName, categoryName, params) {
	var xtick = 1;
	if(categoryName=="Load") {
		xtick = 2;
	} else if(categoryName=="Time") {
		xtick = 0.01;
	}
	$.ajax({
		'type': 'POST',
                'url': 'metrics_data',
                'contentType': 'application/json',
                'data': params,
                'dataType': 'json',
                'complete': function(xhrObj, msg){
                	//console.log(xhrObj);
                        var values = JSON.parse(xhrObj.responseJSON.data);
                        //console.log(values);
			if(values.length>0) {
                        	buildD3Histogram('#canvasD3[data-experiment="'+experimentName+'"]', xtick, values);
			} else {
				$('#canvasD3[data-experiment="'+experimentName+'"]').text("Data unavailable.")
			}
		 }
	});

}

function buildD3Histogram(canvasSelector, tickScale, histValues) {
	$(canvasSelector).empty();

	// Generate a Bates distribution of 10 random variables.
	//var values = d3.range(1000).map(d3.random.bates(10));
	var values = histValues;

	var minVal = Math.floor(Math.min.apply(Math, values));
	var maxVal = Math.ceil(Math.max.apply(Math, values));

	// A formatter for counts.
	var formatCount = d3.format(",.0f");

	var margin = {top: 10, right: 30, bottom: 30, left: 30},
    	//width = 960 - margin.left - margin.right,
	width = $(canvasSelector).width(),
    	//height = 500 - margin.top - margin.bottom;
	height = 320;

	var x = d3.scale.linear()
    		.domain([0, maxVal+minVal])
    		.range([0, width]);

	// Generate a histogram using twenty uniformly-spaced bins.
	var data = d3.layout.histogram()
    			.bins(x.ticks((maxVal+minVal)*tickScale))
    			(values);

	var y = d3.scale.linear()
    		.domain([0, d3.max(data, function(d) { return d.y; })])
    		.range([height, 0]);

	var xAxis = d3.svg.axis()
    		.scale(x)
    		.orient("bottom");

	var svg = d3.select(canvasSelector).append("svg")
    		.attr("width", width + margin.left + margin.right)
    		.attr("height", height + margin.top + margin.bottom)
  		.append("g")
    		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	var bar = svg.selectAll(".bar")
    		.data(data)
  		.enter().append("g")
    		.attr("class", "bar")
    		.attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

	bar.append("rect")
    		.attr("x", 1)
    		.attr("width", x(data[0].dx) - 1)
    		.attr("height", function(d) { return height - y(d.y); });

	bar.filter(function(d) { return d.y>0; })
		.append("text")
    		.attr("dy", ".75em")
    		.attr("y", 6)
    		.attr("x", x(data[0].dx) / 2)
    		.attr("text-anchor", "middle")
    		.text(function(d) { return formatCount(d.y); });

	svg.append("g")
    		.attr("class", "x axis")
    		.attr("transform", "translate(0," + height + ")")
    		.call(xAxis);
}
