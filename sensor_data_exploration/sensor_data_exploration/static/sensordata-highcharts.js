//def xdata_chart() {
$(function () {
    
    var dataArray1 = [];
    var dataArray2 = [];
    var dataArray3 = [];
    
    //    var n_points = context['xdata'].length;
    //    if (context['ydata'].length < n_points) {
    //	n_points = context['ydata'].length;
    //    }
    var n_points = 0;
    var json_ydata = jsonydata
    console.log("jsonydata =");
    console.log(json_ydata);
    n_points = json_ydata.length;

    console.log("n_points is ")
    console.log(n_points)
    for (i = 0; i < n_points; i++) {
	//	dataArray.append([ context['xdata'][i], context['ydata'][i] ]);
	dataArray1.push( [Date.UTC(1970, 1, i), json_ydata[i]]);
	dataArray2.push( [Date.UTC(1970, 1, i), i+5]);
	dataArray3.push( [Date.UTC(1970, 1, i), i-5]);
	console.log("i is ");
	console.log(i);
    }
    console.log("dataArray1=");
    console.log(dataArray1);
	
    $('#container').highcharts({
            chart: {
                type: 'spline'
            },
            title: {
                text: 'Snow depth at Vikjafjellet, Norway'
            },
            subtitle: {
                text: 'Irregular time data in Highcharts JS'
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
                    text: 'Snow depth (m)'
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
            }, {
                name: 'Winter 2008-2009',
                data: dataArray2
            }, {
                name: 'Winter 2009-2010',
                data: dataArray3
            }]
        });
    });
    
