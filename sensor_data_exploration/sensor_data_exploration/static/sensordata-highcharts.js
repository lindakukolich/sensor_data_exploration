function sensordata_chart(title, subtitle, units, short_units, dataArray1, rendor_to, line_color) {
    //Its getting confusing to just keep putting variables in in order. Should we refactor to use a JSON or Dict? - CM
    console.log('about to crate chart to put in ' + rendor_to);
    // Get the graph extremes
    var startDate =new Date(window.starttime);
    var startUTC = startDate.getTime() + startDate.getTimezoneOffset() * 60000;
    var endDate = new Date(window.endtime);
    var endUTC = endDate.getTime() + endDate.getTimezoneOffset() * 60000;

    var chart = new Highcharts.Chart({
        chart: {
	    renderTo: rendor_to,
            type: 'spline' 
        },
        title: {
            text: null
        },
        subtitle: {
            text: null
        },
        xAxis: {
	    min: startUTC,
	    max: endUTC,
	    title: {
		text: null
	    }
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
	    color: line_color,
	    data: dataArray1
	}]
    });
    return chart;
}

function ajax_make_chart(sensorid, starttime, endtime) {
    console.log('GetJSON for ' + sensorid + ' starttime: ' +starttime);
    $.getJSON('/explorer/get_data_ajax/',{'sensorid': sensorid, 'starttime': starttime, 'endtime': endtime})
	.done(function(data) {
	    //make the div use chart-row template
	    var chart_source = $('#chart-row').html();
	    var chart_template = Handlebars.compile(chart_source); //I wonder if I really need to be doing this compile over and over again like this?
	    var legend_data = {
		sensorid: sensorid,
		title: data.plot_short_name,
		subtitle: data.plot_source_id,
		units: data.plot_units_short+' '+data.plot_units_long
	    };
	    $('#charts').append(chart_template(legend_data));
	    var chart_id = sensorid + "-chart";
	    if (data.goodPlotData) {
		var chart = sensordata_chart(data.plot_short_name, data.plot_source_id, data.plot_units_long, data.plot_units_short, data.data_array1, chart_id, data.line_color);
		chartList[sensorid] = chart;

//		console.log(chartList);
//		syncronizeCrossHairs(chart);
		$('.'+sensorid).button('reset');  //Reset the loading on the button
	    } else {
		var errorClass = 'alert alert-warning';
		$('#'+chart_id).html('<div class="' + errorClass + '" >'+data.plotError+'</div>');
		$('.'+sensorid).button('reset');  //Reset the loading on the button
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

function syncZoom(zoomEvent) {

    var min = zoomEvent.min;
    console.log('syncZoom Ran!' + min);
}
