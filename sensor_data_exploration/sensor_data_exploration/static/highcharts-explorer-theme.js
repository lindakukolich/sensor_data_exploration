/**
 * Grid theme for Highcharts JS
 * @author Torstein Honsi
 */

//This will be modified to help us get the look we want our of highcharts for Explorer.

Highcharts.theme = {
    global: {
	timezoneOffset: 5*60
    },
    colors: ['#058DC7', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
    chart: {
	backgroundColor: {
	    linearGradient: { x1: 0, y1: 0, x2: 1, y2: 1 },
	    stops: [
		[0, 'rgb(255, 255, 255)'],
		[1, 'rgb(240, 240, 255)']
	    ]
	},
	borderWidth: 0,
	plotBackgroundColor: 'rgba(255, 255, 255, .9)',
	plotShadow: false,
	plotBorderWidth: 0,
	height: 150,
	zoomType: 'x',
	marginTop: 10,
	marginBottom: 30,
	marginLeft: 30,
    },
    loading: {
        labelStyle: {
            top: '45%'
        }
    },
    title: {
	style: {
	    color: '#000',
	    font: 'bold 16px "Trebuchet MS", Verdana, sans-serif',
	    style: '200px'
	},
	align: 'left',
	verticalAlign: 'top'
    },
    subtitle: {
	align: 'left',
	y: 50,
	style: {
	    color: '#666666',
	    font: 'bold 12px "Trebuchet MS", Verdana, sans-serif',
	    style: '200px'
	}
    },
    xAxis: {
	type: 'datetime',
	dateTimeLabelFormats: {
            hour: '%e-%b %H:%M',
	    day: '%e-%b-%y'
            },
	gridLineWidth: 1,
	lineColor: '#000',
	tickColor: '#000',
	labels: {
	    enabled: true
	},
	title: {
	    text: null
	},
	events: {
            afterSetExtremes: function(zoomEvent) {
		syncZoom(zoomEvent);
	    }
	}
    },
    yAxis: {
	minorTickInterval: 'auto',
	endOnTick: false,
	lineColor: '#000',
	lineWidth: 1,
	tickWidth: 1,
	tickColor: '#000',
	labels: {
	    style: {
		color: '#000',
		font: '11px Trebuchet MS, Verdana, sans-serif'
	    }
	},
	title: {
	    style: {
		color: '#333',
		fontWeight: 'bold',
		fontSize: '12px',
		fontFamily: 'Trebuchet MS, Verdana, sans-serif'
	    }
	}
    },
    legend: {
	enabled: false
    },
    labels: {
	style: {
	    color: '#99b'
	}
    },
    navigation: {
	buttonOptions: {
	    theme: {
		stroke: '#CCCCCC'
	    }
	}
    },
    plotOptions: {
        series: {
            cursor: 'pointer',
            point: {
                events: {
                    click: function(pointEvent) {
			var sensorId = this.series.userOptions.sensorId;
			var x = this.x
			pointClicked(x,sensorId);
                    }
                }
            }
        }
    },
        
   
};

// Apply the theme
var highchartsOptions = Highcharts.setOptions(Highcharts.theme);


