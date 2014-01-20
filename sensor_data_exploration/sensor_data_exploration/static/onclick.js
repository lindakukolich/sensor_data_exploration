$(function () {
    //For bottom tabs
    $('#btn-tabs a').click(function (e) {
	e.preventDefault()
	$(this).tab('show')
    })


    //set up a variable to keep all the charts in, we need to iterate over them to set up the crosshairs.
    window.chartList = []

    //Set up initial graphs: 
    var initial_sensors = ['wu_ti_temp_f', 'bouy5_AirTemp', 'bouy5_WaterTemp'];
    initial_sensors.forEach(function(sensorid) {
	    $('.'+sensorid).addClass('btn-primary');
	    $('.'+sensorid).removeClass('btn-default');
	    ajax_make_chart(sensorid);
	});
    	

	/* If the click came from one of the "sensor" buttons, make a graph
       for that sensor */
    $('.graph-btn').click(function(){
	var sensorid;
	sensorid = $(this).attr('data-sensorid');
	console.log('button clicked: ' + sensorid)
	if ($("#" + sensorid).length != 0) { // This checks to see if a div called sensorid exists already.
	    // To remove a chart. Remove the div. Change the button classes back. 
	    // I bet this needs to get refactored so that it can also be called when you click the "x" from issue 8.
	    console.log('about to remove: ' + sensorid);
	    $("#" + sensorid).remove()
	    $('.'+sensorid).addClass('btn-default');
	    $('.'+sensorid).removeClass('btn-primary');
	} else {
	    $('.'+sensorid).addClass('btn-primary');
	    $('.'+sensorid).removeClass('btn-default');
	    ajax_make_chart(sensorid);
	};
    });
});

