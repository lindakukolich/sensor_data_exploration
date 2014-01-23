/* This function is called automatically when the page is fully loaded */
$( function () {
    //For bottom tabs
    $( '#btn-tabs a' ).click( function (e) {
	e.preventDefault();
	$( this ).tab( 'show' );
    });


    //set up a variable to keep all the charts in, we need to iterate over them to set up the crosshairs.
    //CM - we should see if we can find a way to do this without having the programmer keep track.
    window.chartList = {};

    // set up variables to keep the timestamp range in
    window.starttime = "2014-01-01";
    window.endtime = "2014-01-03";
    /*
      $("#startdatepicker").datepicker("setDate", window.starttime);
      $("#enddatepicker").datepicker("setDate", window.endtime);
    */
    // TODO: Make this use today and yesterday
    //    changeStartTime( 1 );

    //Set up initial graphs: 
    var initial_sensors = ['wu_ti_temp_f', 'bouy5_AirTemp', 'bouy5_WaterTemp'];
    initial_sensors.forEach( function( sensorid ) {
	    $( '.' + sensorid ).addClass( 'btn-primary' );
	    $( '.' + sensorid ).removeClass( 'btn-default' );
	    ajax_make_chart( sensorid, window.starttime, window.endtime );
	});
    	

    /** Register the callback that handles clicks on the graph buttons */
    $( '.graph-btn' ).click( function(){
	    /* If the click came from one of the "sensor" buttons, make a graph
	       for that sensor */
	var sensorid;
	sensorid = $( this ).attr( 'data-sensorid' );
	$( '.' + sensorid ).button( 'loading' );

	console.log( 'button clicked: ' + sensorid )
	if ($( "#" + sensorid ).length != 0) {
	    // This checks to see if a div called sensorid exists already.
	    // To remove a chart. Remove the div. Change the button classes back. 
	    // I bet this needs to get refactored so that it can also be called when you click the "x" from issue 8.
	    console.log( 'about to remove: ' + sensorid );
	    remove_chart_and_manipulate_buttons( sensorid );
	} else {
	    make_chart_and_manipulate_buttons( sensorid );
	};
	
	});

    /**
      Change the date range to be from 'graph_days' ago till now
      Update all the currently displayed graphs
      TODO:
       Update currently displayed start and end times
     */
    $(".time-btn").click(function(){
	change = $(this).attr('graph_days');
	console.log('days to graph: ' + change);
	changeStartTime(change);
	
	console.log('about to loop through chartList' + window.chartList);
	for(var s_id in window.chartList) {
	    var chartIndex = $("#"+s_id+"-chart").data('highchartsChart');
	    console.log('chartIndex is' + chartIndex +"for " + s_id);	    
	    var thisChart = Highcharts.charts[chartIndex];
	    thisChart.showLoading();
	    $('.'+s_id).button('loading');


	    $.getJSON('/explorer/get_data_ajax/',{'sensorid': s_id, 'starttime': starttime, 'endtime': endtime})
		.done(function(data) {
		    if (data.goodPlotData) {

			var chartIndex = $("#"+data.sensor_id+"-chart").data('highchartsChart');

			var thisChart = Highcharts.charts[chartIndex];
			thisChart.series[0].setData(data.data_array1,true);
			thisChart.hideLoading();

			$('.'+data.sensor_id).button('reset');  //Reset the loading on the button
		    } else {
			$('#'+'data.sensor_id'+'-chart').append("<br /><b>" + data.plotError +"</b><br />");
			$('.'+data.sensor_id).button('reset');  //Reset the loading on the button
		    }
		})
		.fail(function(jqxhr, textStatus, error) {
		    var err = textStatus + ", " + error;
		    console.log( "Request Failed: " + err );
		});
	};
    /*
    $( "#dateSelSaveBtn" ).click(function() {
	    var startDate = $("#startdatepicker").datepicker("getDate");
	    var endDate = $("#enddatepicker").datepicker("getDate");
	    if (startDate < endDate) {
		window.starttime = printDate( startDate );
		$("#startdate").html(window.starttime);
		window.endtime = printDate( endDate );
		$("#enddate").html(window.endtime);
		console.log("Change graphs to go from " + window.starttime + " to " + window.endtime);

		for (var s_id in window.chartList) {
		    remove_chart_and_manipulate_buttons(s_id);
		    make_chart_and_manipulate_buttons(s_id);
		}
	    } else {
		console.log("dates are bad. Do not use them");
	    }
	});
    */
    });


    $("#unzoom").click(function(){
	// Unzoom all the charts
	console.log('startin unzoom')

	var endDate = new Date(window.endtime);
	var endUTC = endDate.getTime() + endDate.getTimezoneOffset() * 60000;
	var startDate =new Date(window.starttime);
	var startUTC = startDate.getTime() + startDate.getTimezoneOffset() * 60000;

	$('div#charts > div').each(function() {
	    s_id = $(this).attr('data-sensorid');
	    console.log('going to unzome the following: ' + s_id);
	    var chartIndex = $("#"+s_id+"-chart").data('highchartsChart');
	    var thisChart = Highcharts.charts[chartIndex];
	    thisChart.options.chart.isZoomed = false;

	    thisChart.xAxis[0].setExtremes(startUTC, endUTC, true);
//	    thisChart.xAxis[0].setExtremes(null, null);
	});
    });
});


/**
   Change window.endtime to now.
   Change window.starttime to this number of days before now
*/
function changeStartTime(days) {
    var today = new Date();
    var starttime = today.getTime();
    starttime -= days * 24 * 3600 * 1000;
    var startday = new Date(starttime);
    window.endtime = printDate( today );
    window.starttime = printDate( startday );
    $("#startdate").html(window.starttime);
    $("#enddate").html(window.endtime);
    /*
      $("#startdatepicker").datepicker("setDate", window.starttime);
      $("#enddatepicker").datepicker("setDate", window.endtime);
    */
}

/**
   Print the given Date in the format the database will expect

   TODO: Add time zone and make sure it is GMT
 */
function printDate( d ) {
    var rtn = "";
    var t;
    rtn += d.getFullYear();
    t = d.getMonth() + 1;
    rtn += ((t < 10) ? "-0" : "-") + t;
    t = d.getDate();
    rtn += ((t < 10) ? "-0" : "-") + t + " ";
    t = d.getHours();
    rtn += ((t < 10) ? "0" : "") + t + ":";
    t = d.getMinutes();
    rtn += ((t < 10) ? "0" : "") + t;
    return rtn;
}

/**
   Make the sensorid button display a loading message till the chart is
   displayed
 */
function make_chart_and_manipulate_buttons( sensorid ) {
    $( '.'+sensorid ).button( 'loading' );
    $( '.'+sensorid ).addClass( 'btn-primary' );
    $( '.'+sensorid ).removeClass( 'btn-default' );
    $.when( ajax_make_chart( sensorid, window.starttime, window.endtime ))
	.done( function() {
		$( '.'+sensorid ).button( 'reset' );
	    });
}

/**
   Delete charts and play with the buttons to keep users from clicking
   too often and to make sure they get colored right
 */
function remove_chart_and_manipulate_buttons( sensorid ) {
    $( "." + sensorid ).remove();
    $( '.' + sensorid ).addClass( 'btn-default');
    $( '.' + sensorid ).removeClass( 'btn-primary');
    //Arbitrarily make the loading show up for half a second to discourage double clicking.
    setTimeout( function () {
	    $( '.'+sensorid ).button( 'reset' );
	}, 500);
}
