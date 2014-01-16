$(function () {
    /* Add a check of goodPlotDdata, so we can print an error message here if there is no plot */
    var my_xdata = jQuery.parseJSON(jsonxdata);
    console.log("xdata=", my_xdata);
    var my_ydata = jQuery.parseJSON(jsonydata);
    console.log("ydata=".my_ydata);
    var chart = sensordata_chart(plot_title, plot_subtitle, plot_yaxis_label, plot_point_label, my_xdata, my_ydata);
});

function sensordata_chart(title, subtitle, units, short_units, xdata, ydata) {

    var dataArray1 = [];
    
    var n_points = 0;
    n_points = ydata.length;

    if (n_points > xdata.length) {
	n_points = xdata.length;
    }

    for (i = 0; i < n_points; i++) {
	//	dataArray1.push( [Date.UTC(1970, 1, i), ydata[i]]);
	dataArray1.push( [xdata[i], ydata[i]]);
    }
	
    var chart = new Highcharts.Chart({
            chart: {
		renderTo: 'ourdata',
                type: 'spline'
            },
            title: {
                text: title
            },
            subtitle: {
                text: subtitle
            },
            xAxis: {
                type: 'datetime',
		title: {
		    text: "Date and Time"
		},
            },
            yAxis: {
                title: {
                    text: units
                },
                min: 0
            },
            tooltip: {
                formatter: function() {
		    return '<b>'+ this.series.name +'</b><br/>'+
		    Highcharts.dateFormat('%Y/%m/%d %H:%M', this.x) +': '+ this.y +' ' + short_units;
                }
            },
            
            series: [{
		name: title,
		data: dataArray1
	    }]
        });
    return chart;
}
