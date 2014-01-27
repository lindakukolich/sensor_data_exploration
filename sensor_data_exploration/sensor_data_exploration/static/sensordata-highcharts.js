function sensordata_chart(title, subtitle, units, short_units, dataArray1, sensorId, line_color, url_list) {
    //Its getting confusing to just keep putting variables in in order. Should we refactor to use a JSON or Dict? - CM
    var chartId = sensorId + "-chart";
    // Get the graph extremes

    console.log(dataArray1);
    //Find an existing graph and get it from that graph. This means that if the user has zoomed the new graph will come in at the same zoom.
    var endUTC = 0;
    var startUTC = 0;
    $('div#charts > div').each(function() {
	    var s_id = $(this).attr('data-sensorid');
	var chartIndex = $("#"+s_id+"-chart").data('highchartsChart');
	console.log('chartindex is' + chartIndex);
	if (typeof chartIndex === 'number') {    //error messages will have undefined chartIndex
	    var thisChart = Highcharts.charts[chartIndex];
	    var thisXAxis = thisChart.xAxis[0].getExtremes();
	    startUTC = thisXAxis.min;
	    endUTC = thisXAxis.max;
	    return false;
	};
    });
    console.log('endUTC = ' + endUTC);

    if (endUTC < 1) {
	//There are no charts on the page. We should now check to see if a button is set. But for now I'm just going to default to are start times, today and -7 days.
	var endDate = new Date();
	var endUTC = endDate.getTime() + endDate.getTimezoneOffset() * 60000;
	var startUTC = endUTC - (7 * 24 * 3600 *1000);
    }

    console.log('Chart new startUTC=' + startUTC + ' endUTC =' + endUTC);
    var chart = new Highcharts.Chart({
        chart: {
	    renderTo: chartId,
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
		    return '<b>'+ this.series.name +'</b><br/>'+ Highcharts.dateFormat('%e-%b-%Y %H:%M', this.x) +': '+ this.y +' ' + short_units
            }
        },   
        series: [{
	    name: title,
	    sensorId: sensorId,
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
	    
	    if (data.goodPlotData) {
		var chart = sensordata_chart(data.plot_short_name, data.plot_source_id, data.plot_units_long, data.plot_units_short, data.data_array1, sensorid, data.line_color, data.url_list);

//		syncronizeCrossHairs(chart);
		$('.'+sensorid).button('reset');  //Reset the loading on the button
	    } else {
		var errorClass = 'alert alert-warning';
		var chartId = data.plot_source_id + "-chart";
		$('#'+chartId).html('<div class="' + errorClass + '" >'+data.plotError+'</div>');
		$('.'+sensorid).button('reset');  //Reset the loading on the button
	    }
	})
	.fail(function(jqxhr, textStatus, error) {
	    var err = textStatus + ", " + error;
	    console.log( "Request Failed: " + err );
	});
	$('body').animate({"scrollTop": $(document).height()}, "slow");
};

function syncZoom(zoomEvent) {

    var min = zoomEvent.min;
    var max = zoomEvent.max;

    //let run through all the charts and set them all to this min/max
    $('div#charts > div').each(function() {
	    var s_id = $(this).attr('data-sensorid');
	    var chartIndex = $("#"+s_id+"-chart").data('highchartsChart');
	    console.log('chartindex is' + chartIndex);
	    if (typeof chartIndex === 'number') {    //error messages will have undefined chartIndex
		var thisChart = Highcharts.charts[chartIndex];
		var thisXAxis = thisChart.xAxis[0].getExtremes();
		console.log(s_id + ' min is ' + thisXAxis.min + ' min is ' + min);
		console.log(s_id + ' max is ' + thisXAxis.max + ' max is ' + max);
		if (thisXAxis.min !== min ||
		    thisXAxis.max !== max) {
		    thisChart.xAxis[0].setExtremes(min, max, true);
		}
	    }
    });
}

function pointClicked(x,sensorId) {

    console.log('x= '+ x + ' pointClicked! senosrId ' + sensorId);
    $.getJSON('/explorer/get_point_ajax/',{'sensorid': sensorId, 'x': x})
	.done(function(data) {
	    if (data.value_is_number) {
		console.log('someone clicked a point that is just a number. Ignore this.');
	    } else {
		console.log(data);
		$('#myModal').modal('show');
	    };
	});
}
