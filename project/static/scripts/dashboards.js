/**
 * @author Batch Themes Ltd.
 */
function animateButton(element) {
    $(element).toggleClass('fa-spin');
    setTimeout(function() {
        $(element).removeClass('fa-spin');
    }, 2000);
};

function gauge(element, colors, palette) {
    var opts2 = {
        lines: 12,
        angle: 0.05,
        lineWidth: 0.40,
        pointer: {
            length: 0.75,
            strokeWidth: 0.025,
            color: palette.darkColor
        },
        limitMax: 'false',
        colorStart: colors.info,
        colorStop: colors.info,
        strokeColor: palette.hoverColor,
        generateGradient: false
    };
    var target2 = document.getElementById(element);
    var gauge2 = new Gauge(target2).setOptions(opts2);
    gauge2.maxValue = 100;
    gauge2.animationSpeed = 10;
    gauge2.set(50);
};

function notify(message, type) {
    if (type === 'success') {
        $.notify(message, {
            className: 'success',
            globalPosition: 'top right',
            autoHideDelay: 5000,
        });
    } else if (type === 'info') {
        $.notify(message, {
            className: 'info',
            globalPosition: 'top right',
            autoHideDelay: 5000,
        });
    } else if (type === 'warn' || type === 'warning') {
        $.notify(message, {
            className: 'warn',
            globalPosition: 'top right',
            autoHideDelay: 5000,
        });
    } else if (type === 'error' || type === 'danger') {
        $.notify(message, {
            className: 'error',
            globalPosition: 'top right',
            autoHideDelay: 5000,
        });
    }
};

function chartistPieChart4(element) {
    var data = {
        series: [20, 10, 30, 40]
    };
    var options = {
        donut: true
    };
    new Chartist.Pie(element, data, options);
};

function chartistPieChart3(element) {
    var data = {
        series: [20, 10, 30, 40]
    };
    new Chartist.Pie(element, data);
};

function chartistPieChart2(element) {
    var data = {
        series: [5, 3, 4]
    };

    var sum = function(a, b) {
        return a + b;
    };

    var options = {
        labelInterpolationFnc: function(value) {
            return Math.round(value / data.series.reduce(sum) * 100) + '%';
        }
    };
    new Chartist.Pie(element, data, options);
};

function chartistPieChart1(element) {

    var data = {
        labels: ['Bananas', 'Apples', 'Grapes'],
        series: [20, 15, 40]
    };

    var options = {
        labelInterpolationFnc: function(value) {
            return value[0];
        }
    };

    var responsiveOptions = [
        ['screen and (min-width: 640px)', {
            chartPadding: 30,
            labelOffset: 100,
            labelDirection: 'explode',
            labelInterpolationFnc: function(value) {
                return value;
            }
        }],
        ['screen and (min-width: 1024px)', {
            labelOffset: 80,
            chartPadding: 20
        }]
    ];
    new Chartist.Pie(element, data, options, responsiveOptions);
};

function chartistHalfPieChart(element) {
    var data = {
        series: [20, 10, 30, 40]
    };
    var options = {
        donut: true,
        donutWidth: 60,
        startAngle: 270,
        total: 200,
        showLabel: false
    };
    new Chartist.Pie(element, data, options);
};

function chartistLineChart(element) {

    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min)) + min;
    }

    function pushLimit(arr, elem, limit) {
        arr.push(elem);
        if (arr.length > limit) {
            arr.splice(0, 1);
        }
        return arr;
    }

    var labelsChart1 = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var labels = [];
    var seriesA = [];
    var seriesB = [];
    var points = 8;
    for (var i = 0; i < points; i++) {
        labels.push(labelsChart1[i]);
        seriesA.push(getRandomInt(20, 90));
        seriesB.push(getRandomInt(20, 90));
    }
    var data = {
        labels: labels,
        series: []
    };
    data.series.push(seriesA);
    data.series.push(seriesB);

    var responsiveOptions = [
        ['screen and (max-width: 640px)', {
            axisX: {
                labelInterpolationFnc: function(value) {
                    return value[0];
                }
            }
        }]
    ];

    var chartOptions = {
        showArea: false,
        showLine: true,
        showPoint: true,
        lineSmooth: true,
        low: 0,
        high: 100,
        fullWidth: true,
        height: 200,
        horizontalBars: false,
        chartPadding: {
            left: 0,
            top: 20,
            right: 30,
            bottom: 0
        },
        axisY: {
            showLabel: true,
            showGrid: false
        },
        axisX: {
            showLabel: true,
            showGrid: false
        }
    };

    var chart = new Chartist.Line(element, data, chartOptions, responsiveOptions);

    setInterval(function() {
        var copy = labels;
        var first = copy.shift();
        labels = pushLimit(labels, first, 20);

        data.series[0] = pushLimit(data.series[0], getRandomInt(20, 90), points);
        data.series[1] = pushLimit(data.series[1], getRandomInt(20, 90), points);
        chart.update(data);
    }, 1000);

};

function chartistAreaChart(element) {

    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min)) + min;
    }

    function pushLimit(arr, elem, limit) {
        arr.push(elem);
        if (arr.length > limit) {
            arr.splice(0, 1);
        }
        return arr;
    }

    var labelsChart1 = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var labels = [];
    var seriesA = [];
    var seriesB = [];
    var points = 8;
    for (var i = 0; i < points; i++) {
        labels.push(labelsChart1[i]);
        seriesA.push(getRandomInt(20, 90));
        seriesB.push(getRandomInt(20, 90));
    }
    var data = {
        labels: labels,
        series: []
    };
    data.series.push(seriesA);
    data.series.push(seriesB);

    var responsiveOptions = [
        ['screen and (max-width: 640px)', {
            axisX: {
                labelInterpolationFnc: function(value) {
                    return value[0];
                }
            }
        }]
    ];

    var chartOptions = {
        showArea: true,
        showLine: false,
        showPoint: false,
        lineSmooth: true,
        low: 0,
        high: 100,
        fullWidth: true,
        height: 200,
        horizontalBars: false,
        chartPadding: {
            left: 0,
            top: 20,
            right: 30,
            bottom: 0
        },
        axisY: {
            showLabel: true,
            showGrid: false
        },
        axisX: {
            showLabel: true,
            showGrid: false
        }
    };

    var chart = new Chartist.Line(element, data, chartOptions, responsiveOptions);

    setInterval(function() {
        var copy = labels;
        var first = copy.shift();
        labels = pushLimit(labels, first, 20);

        data.series[0] = pushLimit(data.series[0], getRandomInt(20, 90), points);
        data.series[1] = pushLimit(data.series[1], getRandomInt(20, 90), points);
        chart.update(data);
    }, 1000);

};

function chartistBarChart(element) {

    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min)) + min;
    }

    function pushLimit(arr, elem, limit) {
        arr.push(elem);
        if (arr.length > limit) {
            arr.splice(0, 1);
        }
        return arr;
    }

    var labels = [];
    var seriesA = [];
    for (var i = 0; i < 20; i++) {
        labels.push(i);
        seriesA.push(getRandomInt(20, 80));
    }
    var data = {
        labels: labels,
        series: [
            seriesA
        ]
    };

    var chartOptions = {
        low: 0,
        high: 120,
        seriesBarDistance: 10,
        fullWidth: true,
        height: 200,
        horizontalBars: false,
        chartPadding: {
            left: 0,
            top: 0,
            right: 0,
            bottom: 0
        },
        axisY: {
            //offset: 0,
            showLabel: true,
            showGrid: false
        },
        axisX: {
            offset: 0,
            showLabel: false,
            showGrid: false
        }
    };
    var responsiveOptions = [
        ['screen and (max-width: 640px)', {
            seriesBarDistance: 5,
            axisX: {
                labelInterpolationFnc: function(value) {
                    return value[0];
                }
            }
        }]
    ];
    var chart = new Chartist.Bar(element, data, chartOptions, responsiveOptions);

    setInterval(function() {
        var copy = labels;
        var first = copy.shift();
        labels = pushLimit(labels, first, 20);

        data.series[0] = pushLimit(data.series[0], getRandomInt(20, 80), 20);
        chart.update(data);
    }, 1000);

};

function chartJsBarChart(element, colors, palette) {
    var barChartCtx = document.getElementById(element).getContext("2d");
    var barChartData = {
        labels: ["January", "February", "March", "April", "May", "June", "July"],
        datasets: [{
            label: "My First dataset",
            fillColor: colors.success,
            strokeColor: colors.success,
            highlightFill: colors.success,
            highlightStroke: colors.success,
            data: [65, 59, 80, 81, 56, 55, 40]
        }, {
            label: "My Second dataset",
            fillColor: colors.info,
            strokeColor: colors.info,
            highlightFill: colors.info,
            highlightStroke: colors.info,
            data: [28, 48, 40, 19, 86, 27, 90]
        }]
    };
    var barChartOptions = {
        responsive: true,
        scaleFontColor: palette.textColor,
        scaleBeginAtZero: true,
        scaleShowGridLines: true,
        scaleGridLineColor: "rgba(0,0,0,.05)",
        scaleGridLineWidth: 1,
        scaleShowHorizontalLines: true,
        scaleShowVerticalLines: true,
        barShowStroke: true,
        barStrokeWidth: 1,
        barValueSpacing: 0,
        barDatasetSpacing: 0,
        legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].fillColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"
    };
    new Chart(barChartCtx).Bar(barChartData, barChartOptions);
};

function chartJsAreaChart(element, colors, palette) {

    var areaChartCtx = document.getElementById(element).getContext("2d");
    var areaChartData = {
        labels: ["January", "February", "March", "April", "May", "June", "July"],
        datasets: [{
            label: "My First dataset",
            fillColor: colors.danger,
            strokeColor: colors.danger,
            pointColor: colors.danger,
            pointStrokeColor: colors.textColor,
            pointHighlightFill: colors.textColor,
            pointHighlightStroke: colors.danger,
            data: [65, 59, 80, 81, 56, 55, 40]
        }, {
            label: "My Second dataset",
            fillColor: colors.warning,
            strokeColor: colors.warning,
            pointColor: colors.warning,
            pointStrokeColor: colors.textColor,
            pointHighlightFill: colors.textColor,
            pointHighlightStroke: colors.warning,
            data: [28, 48, 40, 19, 86, 27, 90]
        }]
    };

    var areaChartOptions = {
        responsive: true,
        scaleFontColor: palette.textColor,
        scaleShowGridLines: true,
        scaleGridLineColor: "rgba(0,0,0,.05)",
        scaleGridLineWidth: 1,
        scaleShowHorizontalLines: true,
        scaleShowVerticalLines: true,
        bezierCurve: true,
        bezierCurveTension: 0.4,
        pointDot: true,
        pointDotRadius: 4,
        pointDotStrokeWidth: 1,
        pointHitDetectionRadius: 20,
        datasetStroke: true,
        datasetStrokeWidth: 2,
        datasetFill: true,
        legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"
    };
    new Chart(areaChartCtx).Line(areaChartData, areaChartOptions);
};

function easyPieChart(element, size, barColor, trackColor) {
    $(element).easyPieChart({
        barColor: barColor,
        size: size,
        trackColor: trackColor,
        scaleColor: false,
        animate: true,
        lineWidth: 8,
        lineCap: 'square'
    });
};

function worldMap(element, colors, palette) {

    var bubbleMap = new Datamap({
        element: document.getElementById(element),
        scope: 'world',
        projection: 'mercator',
        responsive: true,
        fills: {
            defaultFill: palette.vectorMapBackgroundColor
        },
        geographyConfig: {
            popupOnHover: false,
            highlightOnHover: false,
            borderWidth: 1,
            borderOpacity: 1,
            borderColor: palette.vectorMapHoverBackgroundColor,
            highlightOnHover: true,
            highlightFillColor: palette.vectorMapHoverBackgroundColor,
            highlightBorderColor: palette.vectorMapHoverBackgroundColor,
            highlightBorderWidth: 1,
            highlightBorderOpacity: 1,
            popupTemplate: function(geography, data) {
                return '<div class="hoverinfo">' + geography.properties.name + '</div>';
            }
        }
    });

    var bubbles = [{
        name: 'Africa',
        radius: 25,
        latitude: 0,
        longitude: 0
    }, {
        name: 'Europe',
        radius: 25,
        latitude: 50,
        longitude: 0
    }, {
        name: 'South America',
        radius: 25,
        latitude: -33,
        longitude: -70
    }, {
        name: 'USA',
        radius: 45,
        latitude: 50,
        longitude: -78
    }, {
        name: 'Asia',
        radius: 45,
        latitude: 50,
        longitude: 120
    }, ];

    bubbleMap.bubbles(bubbles, {
        borderWidth: 1,
        borderOpacity: 1,
        borderColor: colors.warning,
        highlightFillColor: colors.warning,
        highlightBorderColor: colors.warning,
        popupTemplate: function(geo, data) {
            return ['<div class="hoverinfo">' + data.name,
                '</div>'
            ].join('');
        }
    });

    window.addEventListener('resize', function() {
        bubbleMap.resize();
    });

};
