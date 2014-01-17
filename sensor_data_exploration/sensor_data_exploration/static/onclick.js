$(function () {
    $( "#newchart" ).click(function() {
	sample_highchart('newchart')
    });
    $('#ajax-graph').click(function(){
	var sensorid;
	sensorid = $(this).attr('data-sensorid');
	console.log('about to try get_data_ajax and sensorid is:');
	console.log(sensorid)
	$.getJSON('/explorer/get_data_ajax/',{'sensorid': sensorid})
	    .done(function(data) {
		console.log('the get_data_ajax ran and the data is:');
		console.log(data);
		console.log(data.ydata);
		var chart = sensordata_chart(data.plot_title, data.plot_subtitle, data.plot_yaxis_label, data.plot_point_label, data.xdata, data.ydata, 'newchart');
		
	    })
	    .fail(function(jqxhr, textStatus, error) {
		var err = textStatus + ", " + error;
		console.log( "Request Failed: " + err );
	    });
	});

});
