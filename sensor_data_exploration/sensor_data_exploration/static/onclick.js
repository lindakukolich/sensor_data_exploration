$(function () {
    $( "#newchart" ).click(function() {
	sample_highchart('newchart')
    });
    $('.btn-default').click(function(){
	var sensorid;
	sensorid = $(this).attr('data-sensorid');
	$(this).addClass('btn-primary');
	$(this).removeClass('btn-default');


	d=document.createElement('div');
	d.setAttribute("id", sensorid);
	$('#charts').append(d)
	console.log('about to try get_data_ajax and sensorid is:');
	console.log(sensorid)
	$.getJSON('/explorer/get_data_ajax/',{'sensorid': sensorid})
	    .done(function(data) {
		var chart = sensordata_chart(data.plot_title, data.plot_subtitle, data.plot_yaxis_label, data.plot_point_label, data.xdata, data.ydata, sensorid);
		
	    })
	    .fail(function(jqxhr, textStatus, error) {
		var err = textStatus + ", " + error;
		console.log( "Request Failed: " + err );
	    });
	});

});
