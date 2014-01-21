/* This function is called automatically when the page is fully loaded */
$(function () {
    //For bottom tabs
    $('#btn-tabs a').click(function (e) {
	e.preventDefault();
	$(this).tab('show');
    });


    //set up a variable to keep all the charts in, we need to iterate over them to set up the crosshairs.
    window.chartList = [];

    // set up variables to keep the timestamp range in
    window.starttime = "2014-01-01 08:00";
    window.endtime = "2014-01-02 08:00";

    //Set up initial graphs: 
    var initial_sensors = ['wu_ti_temp_f', 'bouy5_AirTemp', 'bouy5_WaterTemp'];
    initial_sensors.forEach(function(sensorid) {
	    $('.'+sensorid).addClass('btn-primary');
	    $('.'+sensorid).removeClass('btn-default');
	    ajax_make_chart(sensorid, window.starttime, window.endtime);
	});
    	

    /** Register the callback that handles clicks on the graph buttons */
    $('.graph-btn').click(function(){
	    /* If the click came from one of the "sensor" buttons, make a graph
	       for that sensor */
	var sensorid;
	sensorid = $(this).attr('data-sensorid');
	$('.'+sensorid).button('loading');

	console.log('button clicked: ' + sensorid)
	if ($("#" + sensorid).length != 0) {
	    // This checks to see if a div called sensorid exists already.
	    // To remove a chart. Remove the div. Change the button classes back. 
	    // I bet this needs to get refactored so that it can also be called when you click the "x" from issue 8.
	    console.log('about to remove: ' + sensorid);
	    $("#" + sensorid).remove();
	    $('.'+sensorid).addClass('btn-default');
	    $('.'+sensorid).removeClass('btn-primary');
	    //Arbitrarily make the loading show up for half a second to discourage double clicking.
	    setTimeout(function () {
		$('.'+sensorid).button('reset');
            }, 500);	    
	    
	} else {
	    $('.'+sensorid).button('loading');
	    $('.'+sensorid).addClass('btn-primary');
	    $('.'+sensorid).removeClass('btn-default');
	    $.when(ajax_make_chart(sensorid, window.starttime, window.endtime))
	      .done(function() {
		  $('.'+sensorid).button('reset');
	      });

	};
	
	});

    /**
      Change the date range to be from 'graph_days' ago till now
      TODO:
       Update all the currently displayed graphs
       Update currently displayed start and end times
     */
    $(".time-btn").click(function(){
	    change = $(this).attr('graph_days');
	    console.log('days to graph: ' + change);
	    changeStartTime(change);
	});
    });

/**
   Change window.endtime to now.
   Change window.starttime to this number of days before now
*/
function changeStartTime(days) {
    var today = new Date();
    console.log("From " + days + " days ago to now");
    console.log("end: " + printDate(today));
    var starttime = today.getTime();
    starttime -= days * 24 * 3600 * 1000;
    var startday = new Date(starttime);
    console.log("start: " + printDate(startday));
    window.endtime = printDate(today);
    window.starttime = printDate(startday);
}

/**
   Print the given Date in the format the database will expect
 */
function printDate(d) {
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
