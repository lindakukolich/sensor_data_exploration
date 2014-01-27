/**
   Generate a chart, given all the pieces needed to label one.

   Set the axis limits to match other charts that are currently displayed,
   or the data range selected by the user if there are no charts.
*/
function sensordata_chart(title, subtitle, units, short_units, dataArray1, sensorId, line_color, dataIsNumber, dataType) {
    //Its getting confusing to just keep putting variables in in order. Should we refactor to use a JSON or Dict? - CM

    var chartId = sensorId + "-chart";

    // Get the graph extremes
    console.log(dataArray1);
    var axisTimes = getAxisTimes();

    console.log('Chart new startUTC=' + axisTimes.starttime + ' endUTC =' + axisTimes.endtime);

    //Set up chart for numeric or string value. Eventually we may want to differenciate between mp3 and images here.
    console.log(dataType);
    if (dataType == 'float') {
	var lineWidth = 1;
	symbol = 'circle'
    } else {
	var lineWidth = 0;
	symbol = 'url(https://cdn1.iconfinder.com/data/icons/16x16-free-toolbar-icons/16/camera.png)';
    };
    
    var ymin = null
    var ymax = null
    
    if (units == 'degrees') {
	ymin = 0
	ymax = 360
    }


    console.log('about to call charts for ' + chartId + symbol);
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
	    min: axisTimes.starttime,
	    max: axisTimes.endtime,
	    title: {
		text: null
	    }
        },
        yAxis: {
            title: {
                text: null
            },
	    min: ymin,
	    max: ymax
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
	    lineWidth: lineWidth,
	    marker: {
		symbol: symbol
	    },
	    data: dataArray1
	}]
    });
    console.log('Created the chart about to return it');
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
		units: data.plot_units_short+' '+data.plot_units_long,
		dataSourceSymbol: data.dataSourceSymbol
	    };

	    $('#charts').append(chart_template(legend_data));

	    //set up the listener on the X button in the legend
	    $( '.x-graph-btn' ).click( function(){
		var sensorId;
		sensorId = $( this ).attr( 'data-sensorId' );
		console.log('graph-btn clicked x to remove '+ sensorId);
		remove_chart_and_manipulate_buttons( sensorId );
	    });
	    
	    //	    if (data.goodPlotData) {
		var chart = sensordata_chart(data.plot_short_name, data.plot_source_id, data.plot_units_long, data.plot_units_short, data.data_array1, sensorid, data.line_color, data.dataIsNumber, data.dataType);
		if (data.goodPlotData === false) {
		    console.log("Plot error: " + data.plotError);
		    chart.showNoData(data.plotError);
		}
		$('.'+sensorid).button('reset');  //Reset the loading on the button
		//	    } else {
		//		var errorClass = 'alert alert-warning';
		//		var chartId = data.plot_source_id + "-chart";
		//		$('#'+chartId).html('<div class="' + errorClass + '" >'+data.plotError+'</div>');
		//		$('.'+sensorid).button('reset');  //Reset the loading on the button
		//	    }
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
		var modal_source = $('#pointModal').html();
		var modal_template = Handlebars.compile(modal_source); //I wonder if I really need to be doing this compile over and over again like this?
		var modal_data = {url: data.url};
		console.log(data.url);
		$('#modalHere').append(modal_template(modal_data));
		$('#pointDisplay').modal('show');
	    };
	});
}
/**
 Find an existing graph and get the Axis extremes from that graph.
 This means that if the user has zoomed the new graph will come in at
 the same zoom.

 If there is no existing graph, use the times requested by the user

Returns an object with two fields, startime and endtime
 */
function getAxisTimes() {
    var endUTC = 0;
    var startUTC = 0;
    $('div#charts > div').each(function() {
	    var s_id = $(this).attr('data-sensorid');
	    var chartIndex = $("#"+s_id+"-chart").data('highchartsChart');
	    //	    console.log('chartindex is' + chartIndex);
	    if (typeof chartIndex === 'number') {
		// This is a real chart
		var thisChart = Highcharts.charts[chartIndex];
		var thisXAxis = thisChart.xAxis[0].getExtremes();
		startUTC = thisXAxis.min;
		endUTC = thisXAxis.max;
		// We found one, quit out of the loop
		return false;
	    }
	});
    //    console.log('endUTC = ' + endUTC);

    // If this is still 0, there were no charts to get data from.
    // Use the time range button selection on the graphs web page
    if (endUTC < 1) {
	var graph_limits = getDataTimes();
	startUTC = makeDate(graph_limits.starttime).getTime();
	endUTC = makeDate(graph_limits.endtime).getTime();
    }
    return {starttime: startUTC, endtime: endUTC};
}
