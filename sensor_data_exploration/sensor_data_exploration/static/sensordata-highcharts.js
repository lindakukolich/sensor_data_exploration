$(function () {
    var my_plotdata = jQuery.parseJSON(plotdata);

    var xdata = my_plotdata.xdata;
    console.log("xdata=", xdata);
    var ydata = my_plotdata.ydata;
    console.log("ydata=", ydata);
    var chart = sensordata_chart(my_plotdata.plot_title,
				 my_plotdata.plot_subtitle,
				 my_plotdata.plot_yaxis_label,
				 my_plotdata.plot_point_label,
				 xdata, ydata, 'ourdata');
    });

function sensordata_chart(title, subtitle, units, short_units, xdata, ydata, rendor_to) {

    var dataArray1 = [];
    console.log("ydata=", ydata);
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
		renderTo: rendor_to,
                type: 'spline',
		height: 250,
		zoomType: 'x'
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
