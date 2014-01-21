function sensordata_chart(title, subtitle, units, short_units, xdata, ydata, rendor_to) {

    var dataArray1 = [];
    console.log("ydata=", ydata);
    var n_points = 0;
    n_points = ydata.length;

    if (n_points > xdata.length) {
	n_points = xdata.length;
    }

    for (i = 0; i < n_points; i++) {
	//	dataArray1.push( [Date.UTC(1970, 1, i), ydata[i]]);
	dataArray1.push( [xdata[i], ydata[i]]);
    }
	
    var chart = new Highcharts.Chart({
            chart: {
		renderTo: rendor_to,
                type: 'spline',
            },
            title: {
                text: null
            },
            subtitle: {
                text: null
            },
            xAxis: {
		title: {
		    text: null
		},
            },
            yAxis: {
                title: {
                    text: null
                }
            },
            tooltip: {
                formatter: function() {
		    return '<b>'+ this.series.name +'</b><br/>'+
		    Highcharts.dateFormat('%Y/%m/%d %H:%M', this.x) +': '+ this.y +' ' + short_units;
                }
            },            
            series: [{
		name: title,
		data: dataArray1
	    }]
        });
    return chart;
}

function ajax_make_chart(sensorid, starttime, endtime) {
    $.getJSON('/explorer/get_data_ajax/',{'sensorid': sensorid, 'starttime': starttime, 'endtime': endtime})
	.done(function(data) {
	    //make the div use chart-row template
	    var chart_source = $('#chart-row').html();
	    var chart_template = Handlebars.compile(chart_source); //I wonder if I really need to be doing this compile over and over again like this?
	    var legend_data = {
		sensorid: sensorid,
		title: data.plot_title,
		subtitle: data.plot_subtitle,
		units: data.plot_yaxis_label
	    };
	    $('#charts').append(chart_template(legend_data));
	    var chart_id = sensorid + "-chart";
	    if (data.goodPlotData) {
		var chart = sensordata_chart(data.plot_title, data.plot_subtitle, data.plot_yaxis_label, data.plot_point_label, data.xdata, data.ydata, chart_id);
//		chartList.push(chart);
//		console.log(chartList);
//		syncronizeCrossHairs(chart);

	    } else {
		$('#'+chart_id).append("<br /><b>" + data.plotError +"</b><br />");
	    }
	})
	.fail(function(jqxhr, textStatus, error) {
	    var err = textStatus + ", " + error;
	    console.log( "Request Failed: " + err );
	});
    $('body').animate({"scrollTop": $(document).height()}, "slow");
};

function syncronizeCrossHairs(chart) {
    var container = $(chart.container),
    offset = container.offset(),
    x, y, isInside, report;
	
    container.mousemove(function (evt) {
	    
        x = evt.clientX - chart.plotLeft - offset.left;
        y = evt.clientY - chart.plotTop - offset.top;
        var xAxis = chart.xAxis[0];
        //remove old plot line and draw new plot line (crosshair) for this chart
        var xAxis1 = chart.xAxis[0];
        xAxis1.removePlotLine("myPlotLineId");
        xAxis1.addPlotLine({
            value: chart.xAxis[0].translate(x, true),
            width: 1,
            color: 'red',
            //dashStyle: 'dash',                   
            id: "myPlotLineId"
        });
    });
}
