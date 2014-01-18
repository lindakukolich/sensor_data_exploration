$(function () {
    $( "#newchart" ).click(function() {
	sample_highchart('newchart')
    });
    $('.btn-default').click(function(){
	var sensorid;
	sensorid = $(this).attr('data-sensorid');

	if ($("#" + sensorid).length != 0) { // This checks to see if a div called sensorid exists already.
	    // To remove a chart. Remove the div. Change the button classes back. 
	    $("#" + sensorid).remove()
	    $(this).addClass('btn-default');
	    $(this).removeClass('btn-primary');
	} else {
	    //I am changing the button first because I lose "this" inside the .getJSON.
	    $(this).addClass('btn-primary');
	    $(this).removeClass('btn-default');
	    d=document.createElement('div'); //create a new div we will name sensorid
	    d.setAttribute("id", sensorid);
	    $('#charts').hide().append(d).slideDown('500');
	    $.getJSON('/explorer/get_data_ajax/',{'sensorid': sensorid})
		.done(function(data) {
		    var chart = sensordata_chart(data.plot_title, data.plot_subtitle, data.plot_yaxis_label, data.plot_point_label, data.xdata, data.ydata, sensorid);
		
		})
		.fail(function(jqxhr, textStatus, error) {
		    var err = textStatus + ", " + error;
		    console.log( "Request Failed: " + err );
		});
	};
	});

});
