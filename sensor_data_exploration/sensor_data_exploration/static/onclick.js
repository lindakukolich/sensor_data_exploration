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

	if ($("#" + sensorid).length != 0) { // This checks to see if a div called sensorid exists already.
	    // To remove a chart. Remove the div. Change the button classes back. 
	    // I bet this needs to get refactored so that it can also be called when you click the "x" from issue 8.
	    $("#" + sensorid).remove()
	    $(this).addClass('btn-default');
	    $(this).removeClass('btn-primary');
	} else {
	    $(this).addClass('btn-primary');
	    $(this).removeClass('btn-default');
	    $.getJSON('/explorer/get_data_ajax/',{'sensorid': sensorid})
		.done(function(data) {
		    //make the div use chart-row template
		    var chart_source = $('#chart-row').html();
		    var chart_template = Handlebars.compile(chart_source); //I wonder if I really need to be doing this compile over and over again like this?
		    var legend_data = {
			sensorid: sensorid,
			title: data.plot_title,
			subtitle: data.plot_subtitle,
			units: data.plot_yaxis_label
		    };
		    console.log(legend_data)
		    $('#charts').append(chart_template(legend_data));
		    $('body').animate({"scrollTop": $('#charts')[0].scrollHeight}, "slow");
		    var chart_id = sensorid + "-chart";
		    if (data.goodPlotData) {
			var chart = sensordata_chart(data.plot_title, data.plot_subtitle, data.plot_yaxis_label, data.plot_point_label, data.xdata, data.ydata, chart_id);
		    } else {
			$('#'+chart_id).append("<br /><b>" + data.plotError +"</b><br />");
		    }
		})
		.fail(function(jqxhr, textStatus, error) {
		    var err = textStatus + ", " + error;
		    console.log( "Request Failed: " + err );
		});
	};
    });
});

