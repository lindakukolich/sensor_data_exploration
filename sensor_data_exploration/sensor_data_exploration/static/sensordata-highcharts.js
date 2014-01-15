$(function () {
    var chart = sensordata_chart('Air Temperature', 'wu_ti_temp_f', 'degrees Farenheit');
});

function sensordata_chart(title, subtitle, units) {

    var dataArray1 = [];
    
    var n_points = 0;
    var json_ydata = jQuery.parseJSON(jsonydata);
    console.log("jsonydata =");
    console.log(json_ydata);
    n_points = json_ydata.length;

    console.log("n_points is ");
    console.log(n_points);
    for (i = 0; i < n_points; i++) {
	dataArray1.push( [Date.UTC(1970, 1, i), json_ydata[i]]);
    }
    console.log("dataArray1=");
    console.log(dataArray1);
	
    //    $('#ourdata').highcharts({
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
                dateTimeLabelFormats: { // don't display the dummy year
                    month: '%e. %b',
                    year: '%b'
                }
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
		    Highcharts.dateFormat('%e. %b', this.x) +': '+ this.y +' m';
                }
            },
            
            series: [{
		name: 'Maybe Our data?',
		// Define the data points. All series have a dummy year
		// of 1970/71 in order to be compared on the same x axis. Note
		// that in JavaScript, months start at 0 for January, 1 for February etc.
		data: dataArray1
	    }]
        });
    return chart;
}
