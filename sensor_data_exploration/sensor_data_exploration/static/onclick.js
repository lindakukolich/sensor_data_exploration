/** This function is called automatically when the page is fully loaded. */
$( function () {
    // For Sensor category tabs at bottom (Headliner, All Meterological, etc.)
    $( '#btn-tabs a' ).click( function (e) {
	e.preventDefault();
	$( this ).tab( 'show' );
    });

    /* Change the start time to match the current-time-btn specified
       on the graph page (explorer/index.html) */
    var currentBtn = getCurrentTimeBtn();
    show_button_as_active( currentBtn );
    changeStartTime( $( currentBtn ).attr( "graph-days" ));

    /** Set up initial graphs

	Note: These names need to match sensor names found in the
	database.  There have been bugs in the past where the database
	names have changed and this code has fallen behind
     */
    var initial_sensors = ['wu_ti_temp_c', 'wu_ti_pressure_mb', 'nor_Wind_speed_avg'];
    initial_sensors.forEach( function( sensorid ) {
	    // console.log('setting up initial graph for'+ sensorid);
	    make_chart_and_manipulate_buttons( sensorid );
	});
    	

    /** Register the callback that handles clicks on the buttons that
	request new charts */
    $( '.graph-btn' ).click( function(){
	console.log('graph-btn clicked');
	var sensorid;
	sensorid = $( this ).attr( 'data-sensorid' );
	/* Make EVERYTING that is named sensorid (buttons and charts)
	   say 'loading...' */
	$( '.' + sensorid ).button( 'loading' );

	// console.log( 'button clicked: ' + sensorid )
	if ($( "#" + sensorid ).length !== 0) {
	    // If there is a div for this chart already, remove the chart
	    // console.log( 'about to remove: ' + sensorid );
	    remove_chart_and_manipulate_buttons( sensorid );
	} else {
	    // Otherwise, make the chart
	    make_chart_and_manipulate_buttons( sensorid );
	}
	
    });
   
    /**
       Save a custom date, updating user feed back and existing charts
     */
    $('#save-date').click(function(){
	var newstart = $('#starttimepicker').datepicker('getDate');
	var newend = $('#endtimepicker').datepicker('getDate');
	if (newstart > newend) {
	    var swaptime = newstart;
	    newstart = newend;
	    newend = swaptime;
	}
	//	console.log('custom date start is ' + newstart + " and end is " + newend);
	update_dates(newstart, newend);
	update_existing_charts();
	show_button_as_inactive(getCurrentTimeBtn());
	setCurrentTimeBtn("#custom-btn");
	show_button_as_active("#custom-btn");
    });

    /**
      Change the date range to be from 'graph-days' ago till now
      Update all the currently displayed graphs
    */
    $(".time-btn").click(function() {
	    var change = $(this).attr('graph-days');
	    var currentBtn = getCurrentTimeBtn();
	    show_button_as_inactive(currentBtn);
	    currentBtn = "#" + $(this).attr('id');
	    show_button_as_active(currentBtn);
	    setCurrentTimeBtn(currentBtn);
	    // console.log('days to graph: ' + change);
	    changeStartTime(change);
	    update_existing_charts();
    });

    /**
       Erase all the charts, and un-select all their buttons
     */
    $("#clear").click(function(){
	$('div#charts > div').each(function() {
		var s_id = $(this).attr('data-sensorid');
		remove_chart_and_manipulate_buttons( s_id );
	});
    });

    /**
       Go back to using the Data-time as the axis limits of all the charts
     */
    $("#unzoom").click(function(){
	    // Unzoom all the charts
	    //	console.log('starting unzoom')
	    // We don't use startUTC and EndUTC here because we want to force to window settings.
	    var startEndDates = getDataTimes();
	    console.log("NEW DATE: unzoom: " + startEndDates.starttime + " to " +
			startEndDates.endtime);
	    var startDate = makeDate(startEndDates.starttime);
	    var endDate = makeDate(startEndDates.endtime);
	    var endUTC = endDate.getTime();
	    var startUTC = startDate.getTime();

	$('div#charts > div').each(function() {
		var s_id = $(this).attr('data-sensorid');
	    //	    console.log('going to unzoom the following: ' + s_id);
		var chartIndex = $("#"+s_id+"-chart").data('highchartsChart');
	    //	    console.log('chartindex is' + chartIndex);
	    if (typeof chartIndex === 'number') {    //error messages will have undefined chartIndex
		var thisChart = Highcharts.charts[chartIndex];
		thisChart.xAxis[0].setExtremes(startUTC, endUTC, true);
		return false; // once we set one the sync zoom will set the rest
	    }
	    });
	});
    });

/** This function updates the existing charts on our page with new time
    selectors, which have already been stored in data-start-time and
    data-end-time */
function update_existing_charts() {
    var dataTime = getDataTimes();
    console.log("NEW DATE: update_existing_charts: " + dataTime.starttime + " to " +
		dataTime.endtime);
    var endDate = makeDate(dataTime.endtime);
    var startDate = makeDate(dataTime.starttime);
    // Time zone offset is in minutes, we want 60 * 1000 for ms
    var endUTC = endDate.getTime();
    var startUTC = startDate.getTime();
    console.log("Update UTC from " + startUTC + " to " + endUTC);
	
    $('div#charts > div').each(function() {
	    var s_id = $(this).attr('data-sensorid');
	    var chartIndex = $("#"+s_id+"-chart").data('highchartsChart');
	    //	    console.log('chartIndex is' + chartIndex +"for " + s_id);	  
	    var thisChart = Highcharts.charts[chartIndex];
	    if (typeof chartIndex === 'number') {    //error messages will have undefined chartIndex  
		thisChart.showLoading();
		$('.'+s_id).button('loading');


		$.getJSON('/explorer/get_data_ajax/',{'sensorid': s_id, 'starttime': dataTime.starttime, 'endtime': dataTime.endtime})
		    .done(function(data) {
			    var chartIndex = $("#"+data.sensor_id+"-chart").data('highchartsChart');
			    var thisChart = Highcharts.charts[chartIndex];
			    thisChart.series[0].setData(data.data_array1,false);
			    thisChart.xAxis[0].setExtremes(startUTC, endUTC, true);
			    thisChart.hideLoading();

			    $('.'+data.sensor_id).button('reset');  // Reset the loading on the button
		    })
		    .fail(function(jqxhr, textStatus, error) {
			var err = textStatus + ", " + error;
			//			console.log( "Request Failed: " + err );
		    });
		//need an else here to try again to draw the graph if it had an error in the original time.
	    };
	});
}


/**
   Change data-end-time to now
   Change data-start-time to this number of days before now
*/
function changeStartTime(days) {
    var today = new Date();
    // getTimezoneOffset is in minutes, we want milliseconds for Javascript
    // back up the current time
    var starttime = today.getTime();
    starttime -= days * 24 * 3600 * 1000;
    var startday = new Date(starttime);
    update_dates(startday, today);
}

/**
   Make a Date object from a date in our database format
   2014-01-18 16:28-05:00.

   If we just use new Date, the code only works on Chrome, not Firefox or IE
*/
function makeDate( dateString ){
    var dateTime = dateString.split(/ /);
    var dateParts = dateTime[0].split(/-/);
    var timeAndZone = dateTime[1].split(/[-+]/);
    var timeParts = timeAndZone[0].split(/:/);
    var d = new Date(dateParts[0], dateParts[1] - 1, dateParts[2], timeParts[0], timeParts[1]);
    return d;
}
/**
   Print the given Date in the format the database will expect
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
    // Mark the time zone
    t = d.getTimezoneOffset();
    var tzHr = t/60;
    var tzMin = t % 60;
    /* Why yes, this Timezone adjustment looks like it is backwards.
       This is the number you need to add to local time to match GMT,
       where the +- in the date tells you how far behind GMT your
       local time is
    */
    rtn += ((t > 0) ? "-" : "+") + ((tzHr < 10) ? "0" : "") + tzHr;
    rtn += ":" + ((tzMin < 10) ? "0" : "") + tzMin;
    return rtn;
}

/**
   Print a date in a format people like
*/
function prettyDate( d ) {
    var rtn = "";
    var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    rtn += d.getDate() + "-";
    rtn += months[d.getMonth()] + "-";
    rtn += d.getFullYear();
    return rtn;
}

/**
   Add the time to a prettyDate
 */
function prettyDateTime( d ) {
    var rtn = "";
    rtn = prettyDate(d);
    var t = d.getHours();
    rtn += " " + ((t < 10) ? "0" : "") + t + ":";
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
    show_button_as_active('.'+sensorid);
    var dataTimes = getDataTimes();
    $.when( ajax_make_chart( sensorid, dataTimes.starttime, dataTimes.endtime ))
	.done( function() {
		$( '.'+sensorid ).button( 'reset' );
	    });
}

/**
   Delete charts and play with the buttons to keep users from clicking
   too often and to make sure they get colored right
 */
function remove_chart_and_manipulate_buttons( sensorid ) {
    // Remove the graph
    $( "#" + sensorid + "-chart" ).remove();
    $( "#" + sensorid ).remove();
    show_button_as_inactive('.'+sensorid);
    //Arbitrarily make the loading show up for half a second to discourage double clicking.
    setTimeout( function () {
	    $( '.'+sensorid ).button( 'reset' );
	}, 500);
}

/**
   Store the new start and end dates for graph data in the various
   places that need to know it
*/
function update_dates(startday, endday) {
    // save these dates as an attribute of our graph page
    setDataTimes( printDate( startday ), printDate( endday ));
    // Show the User the dates
    $("#startdate").html( prettyDate( startday ));
    $("#enddate").html( prettyDate( endday ));
    // Update the custom date picker
    $("#endtimepicker").datepicker( 'setDate', endday );
    $("#starttimepicker").datepicker( 'setDate', startday );
}

/**
   Show this button as selected
 */
function show_button_as_active(button_id) {
    $(button_id).addClass( 'btn-primary' );
    $(button_id).removeClass( 'btn-default' );
}

/**
   Show this button as not selected
*/
function show_button_as_inactive(button_id) {
    $(button_id).addClass( 'btn-default');
    $(button_id).removeClass( 'btn-primary');
}

/**
   Get the data time
*/
function getDataTimes(){
    var startTime = $( "#timeselection" ).attr( "data-start-time" );
    var endTime =  $( "#timeselection" ).attr( "data-end-time" );
    return {starttime: startTime, endtime: endTime};
}

/**
   Set the data time as a string with time zone on it
*/
function setDataTimes(starttime, endtime){
    $("#timeselection").attr("data-start-time", starttime);
    $("#timeselection").attr("data-end-time", endtime);
}

/**
   Get the HTML ID of the current time selection button.
   The id is named in explorer/index.html
 */
function getCurrentTimeBtn() {
    return $("#timeselection").attr("current-time-btn");
}
/**
   Store the HTML ID of the current time selection button
*/
function setCurrentTimeBtn(btnId) {
    $("#timeselection").attr("current-time-btn", btnId);
}
