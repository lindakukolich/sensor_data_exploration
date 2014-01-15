$(function () {
    $( "#newchart" ).click(function() {
	sample_highchart('newchart')
    });
    $('#ajax-graph').click(function(){
	var sensorid;
	sensorid = $(this).attr('data-sensorid');
	$.get('/explorer/get_data_ajax/', function(data) {
	    console.log('the get_data_ajax ran!');
	    sample_highchart('newchart');
	    });
	});
});
