$(function () {
    /* If the click came from the "Use AJAX" button, make a copy of
       the sample graph from HighCharts */
    $( "#newchart" ).click(function() {
	sample_highchart('newchart')
    });
    /* If the click came from one of the "sensor" buttons, make a graph
       for that sensor */
    $('.btn-default').click(function(){
	var sensorid;
	sensorid = $(this).attr('data-sensorid');
	$(this).addClass('btn-primary');
	$(this).removeClass('btn-default');

	/* Make a div element to display the graph in */
	d=document.createElement('div');
	d.setAttribute("id", sensorid);
	$('#charts').append(d);
	console.log('about to try get_data_ajax and sensorid is:');
	console.log(sensorid);
	$.getJSON('/explorer/get_data_ajax/',{'sensorid': sensorid})
	    .done(function(data) {
		if (data.goodPlotData) {
		    console.log('the get_data_ajax ran and the data is:');
		    console.log(data);
		    console.log(data.ydata);
		    var chart = sensordata_chart(data.plot_title, data.plot_subtitle, data.plot_yaxis_label, data.plot_point_label, data.xdata, data.ydata, sensorid, d);
		} else {
		    d.innerHTML = "<br /><b>" + data.plotError +"</b><br />";
		}
	    })
	    .fail(function(jqxhr, textStatus, error) {
		var err = textStatus + ", " + error;
		d.innerHTML = "<br /><b>" + textStatus + ", " + error +"</b><br />";
		console.log( "Request Failed: " + err );
	    });
	});

});
