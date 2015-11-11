(function(){
  'use strict';

  var WrapkitUtils = window.WrapkitUtils,
  Chart = window.Chart;

  // default setting
  Chart.defaults.global.responsive = true;
  Chart.defaults.global.scaleLineColor = 'rgba(22, 24, 27, 0.12)';
  Chart.defaults.global.scaleFontColor = 'rgba(22, 24, 27, 0.54)';
  Chart.defaults.global.tooltipFillColor = 'rgba(22, 24, 27, 0.9)';
  Chart.defaults.global.tooltipFontSize = 11;
  Chart.defaults.global.tooltipTitleFontSize = 12;
  Chart.defaults.global.tooltipTitleFontStyle = 600;
  Chart.defaults.global.tooltipCornerRadius = 2;

  // Line Chart
  // Line #1
  var lineCtx = document.getElementById('chartjs-line').getContext('2d'),
  lineData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
      {
        label: 'iPhone',
        fillColor: 'transparent',
        strokeColor: 'rgba(237, 85, 101, 1)',
        pointColor: 'rgba(237, 85, 101, 1)',
        pointStrokeColor: '#ffffff',
        pointHighlightFill: '#ffffff',
        pointHighlightStroke: 'rgba(237, 85, 101, 0.8)',
        data: [65, 59, 80, 81, 56, 55, 40, 70, 53, 56, 79, 61]
      },
      {
        label: 'iPad',
        fillColor: 'transparent',
        strokeColor: 'rgba(79, 193, 233, 1)',
        pointColor: 'rgba(79, 193, 233, 1)',
        pointStrokeColor: '#ffffff',
        pointHighlightFill: '#ffffff',
        pointHighlightStroke: 'rgba(79, 193, 233, 0.8)',
        data: [28, 48, 40, 19, 86, 27, 90, 65, 86, 50, 95, 89]
      }
    ]
  },
  chartjsLine = new Chart(lineCtx).Line(lineData, {
    scaleBeginAtZero: true,
    scaleShowVerticalLines: false,
  });

  // Line #2
  var sin = [],
  cos = [],
  lbl = [],
  n = 0;

  for (var i = 0; i < 7; i += 0.5) {
    sin.push(Math.sin(i));
    cos.push(Math.cos(i));
    lbl.push( n++ );
  }

  var line2Ctx = document.getElementById('chartjs-line2').getContext('2d'),
  line2Data = {
    labels: lbl,
    datasets: [
      {
        label: 'Sin(x)',
        fillColor: 'transparent',
        strokeColor: 'rgba(67, 74, 84, 1)',
        pointColor: 'rgba(67, 74, 84, 1)',
        pointStrokeColor: '#ffffff',
        pointHighlightFill: '#ffffff',
        pointHighlightStroke: 'rgba(67, 74, 84, 0.8)',
        data: sin
      },
      {
        label: 'Cos(x)',
        fillColor: 'rgba(72, 207, 173, 0.2)',
        strokeColor: 'rgba(72, 207, 173, 1)',
        pointColor: 'rgba(72, 207, 173, 1)',
        pointStrokeColor: '#ffffff',
        pointHighlightFill: '#ffffff',
        pointHighlightStroke: 'rgba(72, 207, 173, 0.8)',
        data: cos
      }
    ]
  },
  chartjsLine2 = new Chart(line2Ctx).Line(line2Data, {
    scaleBeginAtZero: false,
    scaleShowVerticalLines: false
  });
  // line #3
  var line3Ctx = document.getElementById('chartjs-line3').getContext('2d'),
  line3Data = {
    labels: lbl,
    datasets: [
      {
        label: 'Sin(x)',
        fillColor: 'transparent',
        strokeColor: 'rgba(67, 74, 84, 1)',
        pointColor: 'rgba(67, 74, 84, 1)',
        pointStrokeColor: '#ffffff',
        pointHighlightFill: '#ffffff',
        pointHighlightStroke: 'rgba(67, 74, 84, 0.8)',
        data: sin
      },
      {
        label: 'Cos(x)',
        fillColor: 'rgba(93, 156, 236, 0.2)',
        strokeColor: 'rgba(93, 156, 236, 1)',
        pointColor: 'rgba(93, 156, 236, 1)',
        pointStrokeColor: '#ffffff',
        pointHighlightFill: '#ffffff',
        pointHighlightStroke: 'rgba(93, 156, 236, 0.8)',
        data: cos
      }
    ]
  },
  chartjsLine3 = new Chart(line3Ctx).Line(line3Data, {
    scaleBeginAtZero: false,
    scaleShowVerticalLines: false
  });


  // Bar Chart
  // Bar #1
  var barCtx = document.getElementById('chartjs-bar').getContext('2d'),
  barData = {
    labels: ['Phone', 'Affiliate', 'Social', 'Mail', 'SE', 'Sales'],
    datasets: [
      { label: 'W1', fillColor: 'rgba(79, 193, 233, 1)', highlightFill: 'rgba(79, 193, 233, 0.8)', data: [915, 729, 620, 801, 516, 365] },
      { label: 'W2', fillColor: 'rgba(72, 207, 173, 1)', highlightFill: 'rgba(72, 207, 173, 0.8)', data: [741, 545, 652, 752, 553, 357] }
    ]
  },
  chartjsBar = new Chart(barCtx).Bar(barData, {
    scaleShowGridLines : false,
    scaleShowVerticalLines: false,
    scaleLineColor: 'transparent',
    barShowStroke : false,
    scaleShowLabels: false,
    barValueSpacing : 12
  });

  // Bar #2 - #4
  var bar2Ctx = document.getElementById('chartjs-bar2').getContext('2d'),
  bar3Ctx = document.getElementById('chartjs-bar3').getContext('2d'),
  bar4Ctx = document.getElementById('chartjs-bar4').getContext('2d'),
  bar2Data = {
    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    datasets: [
      { label: 'Clothes', fillColor: 'rgba(172, 146, 236, 1)', highlightFill: 'rgba(172, 146, 236, 0.8)', data: [98, 80, 64, 56] },
      { label: 'Trousers', fillColor: 'rgba(237, 85, 101, 1)', highlightFill: 'rgba(237, 85, 101, 0.8)', data: [51, 60, 91, 76] }
    ]
  },
  bar3Data = {
    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    datasets: [
      { label: 'Clothes', fillColor: 'rgba(72, 207, 173, 1)', highlightFill: 'rgba(72, 207, 173, 0.8)', data: [65, 59, 80, 81] },
      { label: 'Trousers', fillColor: 'rgba(93, 156, 236, 1)', highlightFill: 'rgba(93, 156, 236, 0.8)', data: [81, 56, 55, 40] }
    ]
  },
  bar4Data = {
    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    datasets: [
      { label: 'Clothes', fillColor: 'rgba(237, 85, 101, 1)', highlightFill: 'rgba(237, 85, 101, 0.8)', data: [65, 59, 80, 81] },
      { label: 'Trousers', fillColor: 'rgba(93, 156, 236, 1)', highlightFill: 'rgba(93, 156, 236, 0.8)', data: [28, 48, 40, 19] }
    ]
  },
  chartjsBar2 = new Chart(bar2Ctx).Bar(bar2Data, {
    scaleShowVerticalLines: false,
    barShowStroke : false,
    barValueSpacing : 16
  }),
  chartjsBar3 = new Chart(bar3Ctx).Bar(bar3Data, {
    scaleShowVerticalLines: false,
    barShowStroke : false,
    barValueSpacing : 16
  }),
  chartjsBar4 = new Chart(bar4Ctx).Bar(bar4Data, {
    scaleShowVerticalLines: false,
    barShowStroke : false,
    barValueSpacing : 16
  });

  // Bar #5
  var bar5Ctx = document.getElementById('chartjs-bar5').getContext('2d'),
  bar5Data = {
    labels: ['Strengths', 'Weaknesses', 'Opportunities', 'Threats'],
    datasets: [
      { label: 'W1', fillColor: 'rgba(93, 156, 236, 1)', highlightFill: 'rgba(93, 156, 236, 0.8)', data: [900, 650, 450, 400] },
      { label: 'W2', fillColor: 'rgba(127, 176, 240, 1)', highlightFill: 'rgba(127, 176, 240, 0.8)', data: [750, 950, 600, 420] },
      { label: 'W3', fillColor: 'rgba(164, 199, 244, 1)', highlightFill: 'rgba(164, 199, 244, 0.8)', data: [600, 420, 750, 950] },
      { label: 'W4', fillColor: 'rgba(200, 221, 249, 1)', highlightFill: 'rgba(200, 221, 249, 0.8)', data: [450, 400, 900, 650] }
    ]
  },
  chartjsBar5 = new Chart(bar5Ctx).Bar(bar5Data, {
    scaleShowGridLines : false,
    scaleShowVerticalLines: false,
    scaleLineColor: 'transparent',
    barShowStroke : false,
    tooltipFillColor: 'rgba(67, 74, 84, 0.8)',
    tooltipFontSize: 11,
    tooltipTitleFontSize: 11,
    tooltipTitleFontStyle: 'normal',
    tooltipCornerRadius: 2,
    barValueSpacing : 14
  });



  // Radar Chart
  // Radar #1
  var radarCtx = document.getElementById('chartjs-radar').getContext('2d'),
  radarData = {
    labels: ['Phone', 'Affiliate', 'Social', 'Mail', 'SE', 'Sales'],
    datasets: [
      {
        label: 'W1',
        fillColor: 'rgba(160, 212, 104, 0.2)',
        strokeColor: 'rgba(160, 212, 104, 1)',
        pointColor: 'rgba(160, 212, 104, 1)',
        pointStrokeColor: '#ffffff',
        pointHighlightFill: 'rgba(160, 212, 104, 1)',
        pointHighlightStroke: '#ffffff',
        data: [59, 90, 81, 56, 55, 40]
      },
      {
        label: 'W2',
        fillColor: 'rgba(255, 206, 84, 0.2)',
        strokeColor: 'rgba(255, 206, 84, 1)',
        pointColor: 'rgba(255, 206, 84, 1)',
        pointStrokeColor: '#ffffff',
        pointHighlightFill: 'rgba(255, 206, 84, 1)',
        pointHighlightStroke: '#ffffff',
        data: [28, 48, 19, 96, 27, 100]
      }
    ]
  },
  chartjsRadar = new Chart(radarCtx).Radar(radarData);



  // Polar Chart
  // Polar #1
  var polarCtx = document.getElementById('chartjs-polar').getContext('2d'),
  polarData = [
    { value: 300, color: '#ED5565', highlight: '#DA4453', label: 'Strengths' },
    { value: 250, color: '#FFCE54', highlight: '#F6BB42', label: 'Weaknesses' },
    { value: 150, color: '#5D9CEC', highlight: '#4A89DC', label: 'Opportunities' },
    { value: 220, color: '#48CFAD', highlight: '#37BC9B', label: 'Threats' }
  ],
  chartjsPolar = new Chart(polarCtx).PolarArea(polarData, { segmentStrokeColor: '#434A54' });



  // Pie Chart
  // Doghnut #1
  var doughnutCtx = document.getElementById('chartjs-doughnut').getContext('2d'),
  doughnutData = [
    { value: 795236, color: '#ED5565', highlight: '#DA4453', label: 'Google+' },
    { value: 542511, color: '#FC6E51', highlight: '#E9573F', label: 'Instagram' },
    { value: 856215, color: '#5D9CEC', highlight: '#4A89DC', label: 'Facebook' },
    { value: 1596854, color: '#4FC1E9', highlight: '#3BAFDA', label: 'Twitter' }
  ],
  chartjsDoughnut = new Chart(doughnutCtx).Doughnut(doughnutData, {
    segmentShowStroke: false
  });

  // Pie #1
  var pieCtx = document.getElementById('chartjs-pie').getContext('2d'),
  pieData = [
    { value: 795236, color: '#ED5565', highlight: '#DA4453', label: 'Google+' },
    { value: 542511, color: '#FC6E51', highlight: '#E9573F', label: 'Instagram' },
    { value: 856215, color: '#5D9CEC', highlight: '#4A89DC', label: 'Facebook' },
    { value: 1596854, color: '#4FC1E9', highlight: '#3BAFDA', label: 'Twitter' }
  ],
  chartjsPie = new Chart(pieCtx).Pie(pieData);


  // update when content width changed (only on desktop for save performance)
  if (!WrapkitUtils.isMobile()) {
    [].forEach.call(['show', 'hide', 'size', 'setMode'], function(ev){
      window.sidebar.on( ev, WrapkitUtils.debounce(function(){
        // manual redraw chart
        // lines
        chartjsLine.resize(chartjsLine.render, true);
        chartjsLine2.resize(chartjsLine2.render, true);
        chartjsLine3.resize(chartjsLine3.render, true);
        // bars
        chartjsBar.resize(chartjsBar.render, true);
        chartjsBar2.resize(chartjsBar2.render, true);
        chartjsBar3.resize(chartjsBar3.render, true);
        chartjsBar4.resize(chartjsBar4.render, true);
        chartjsBar5.resize(chartjsBar5.render, true);
        // radars
        chartjsRadar.resize(chartjsRadar.render, true);
        // polar area
        chartjsPolar.resize(chartjsPolar.render, true);
        // pie
        chartjsDoughnut.resize(chartjsDoughnut.render, true);
        chartjsPie.resize(chartjsPie.render, true);
      }, 250));
    });
    window.wl.on( 'layoutChanged', WrapkitUtils.debounce(function(){
      // manual redraw chart
      // lines
      chartjsLine.resize(chartjsLine.render, true);
      chartjsLine2.resize(chartjsLine2.render, true);
      chartjsLine3.resize(chartjsLine3.render, true);
      // bars
      chartjsBar.resize(chartjsBar.render, true);
      chartjsBar2.resize(chartjsBar2.render, true);
      chartjsBar3.resize(chartjsBar3.render, true);
      chartjsBar4.resize(chartjsBar4.render, true);
      chartjsBar5.resize(chartjsBar5.render, true);
      // radars
      chartjsRadar.resize(chartjsRadar.render, true);
      // polar area
      chartjsPolar.resize(chartjsPolar.render, true);
      // pie
      chartjsDoughnut.resize(chartjsDoughnut.render, true);
      chartjsPie.resize(chartjsPie.render, true);
    }, 250));
  }
})(window);