$(function () {
    $( "#newchart" ).click(function() {
	sample_highchart('newchart')
    });
    $('#ajax-graph').click(function(){
	var sensorid;
	sensorid = $(this).attr('data-sensorid');
	$.getJSON('/explorer/get_data_ajax/',{})
	    .done(function(data) {
		console.log('the get_data_ajax ran and the data is:');
		console.log(data);
		console.log(data.ydata);
		sample_highchart('newchart');
	    })
	    .fail(function(jqxhr, textStatus, error) {
		var err = textStatus + ", " + error;
		console.log( "Request Failed: " + err );
	    });
	});

});
