(function(){
  'use strict';

  var Morris = window.Morris,
  WrapkitUtils = window.WrapkitUtils;

  // Graph Opportunity and winrate
  var graphOpwr = Morris.Area({
    element: 'graph-opwr',
    fillOpacity: 1,
    lineWidth: 0,
    data: [
      { period: '2015-01', asia: 26, ausaf: 30, europe: 24, america: 21 },
      { period: '2015-02', asia: 27, ausaf: 22, europe: 24, america: 28 },
      { period: '2015-03', asia: 49, ausaf: 19, europe: 25, america: 29 },
      { period: '2015-04', asia: 37, ausaf: 35, europe: 56, america: 40 },
      { period: '2015-05', asia: 68, ausaf: 19, europe: 22, america: 32 },
      { period: '2015-06', asia: 56, ausaf: 42, europe: 18, america: 34 },
      { period: '2015-07', asia: 48, ausaf: 37, europe: 15, america: 29 },
      { period: '2015-08', asia: 150, ausaf: 59, europe: 51, america: 84 },
      { period: '2015-09', asia: 106, ausaf: 44, europe: 20, america: 67 },
      { period: '2015-10', asia: 84, ausaf: 57, europe: 17, america: 58 }
    ],
    preUnits: '$',
    postUnits: 'M',
    xkey: 'period',
    xLabelFormat: function (x) {
      var IndexToMonth = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Des' ];
      return IndexToMonth[ x.getMonth() ];
    },
    dateFormat: function (x) {
      x = new Date(x);
      var IndexToMonth = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Des' ];
      return IndexToMonth[ x.getMonth() ];
    },
    ykeys: ['asia', 'ausaf', 'europe', 'america'],
    labels: ['Asia', 'Australia & Africa', 'Europe', 'America'],
    pointSize: 0,
    lineColors: ['#48CFAD', '#4FC1E9', '#5D9CEC', '#AC92EC'],
    grid: false,
    gridTextColor: 'rgba(22, 24, 27, 0.87)',
    hideHover: true,
    resize: true // NOTE: This has a significant performance impact, so is disabled by default.
  });

  var graphSocFol = Morris.Line({
    element: 'graph-socfol',
    fillOpacity: 1,
    lineWidth: 2,
    data: [
      { period: '2015-01', gplus: 26, instagram: 30, twitter: 24, fb: 21 },
      { period: '2015-02', gplus: 27, instagram: 22, twitter: 24, fb: 28 },
      { period: '2015-03', gplus: 49, instagram: 19, twitter: 25, fb: 29 },
      { period: '2015-04', gplus: 37, instagram: 35, twitter: 56, fb: 40 },
      { period: '2015-05', gplus: 68, instagram: 19, twitter: 22, fb: 32 },
      { period: '2015-06', gplus: 56, instagram: 42, twitter: 18, fb: 34 },
      { period: '2015-07', gplus: 48, instagram: 37, twitter: 15, fb: 29 },
      { period: '2015-08', gplus: 150, instagram: 59, twitter: 51, fb: 84 },
      { period: '2015-09', gplus: 106, instagram: 44, twitter: 20, fb: 67 },
      { period: '2015-10', gplus: 84, instagram: 57, twitter: 17, fb: 58 }
    ],
    xkey: 'period',
    xLabelFormat: function (x) {
      var IndexToMonth = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Des' ];
      return IndexToMonth[ x.getMonth() ];
    },
    dateFormat: function (x) {
      x = new Date(x);
      var IndexToMonth = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Des' ];
      return IndexToMonth[ x.getMonth() ];
    },
    ykeys: ['gplus', 'instagram', 'twitter', 'fb'],
    labels: ['Google+', 'Instagram', 'Twitter', 'Facebook'],
    pointSize: 0,
    lineColors: ['#ED5565', '#48CFAD', '#4FC1E9', '#5D9CEC'],
    grid: false,
    gridTextColor: 'rgba(22, 24, 27, 0.54)',
    hideHover: true,
    resize: true // NOTE: This has a significant performance impact, so is disabled by default.
  });

  // upload and download graph
  var graphUpdown = Morris.Bar({
    element: 'graph-updown',
    fillOpacity: 1,
    lineWidth: 0,
    data: [
      { period: '2015-10-11', upload: 2666, download: 1294 },
      { period: '2015-10-12', upload: 2778, download: 2294 },
      { period: '2015-10-13', upload: 4912, download: 1969 },
      { period: '2015-10-14', upload: 3767, download: 3597 },
      { period: '2015-10-15', upload: 6810, download: 1914 },
      { period: '2015-10-16', upload: 5670, download: 4293 },
      { period: '2015-10-17', upload: 4820, download: 3795 }
    ],
    xkey: 'period',
    xLabelFormat: function (data) {
      var x = new Date(data.src.period),
      days = [ 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat' ];
      return days[ x.getDay() ];
    },
    dateFormat: function (data) {
      var x = new Date(data.src.period),
      days = [ 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat' ];
      return days[ x.getDay() ];
    },
    ykeys: ['upload', 'download'],
    labels: ['Upload', 'Download'],
    pointSize: 0,
    hideHover: true,
    barColors: ['#48CFAD', '#FFCE54'],
    grid: false,
    gridTextColor: 'rgba(22, 24, 27, 0.54)',
    resize: true // NOTE: This has a significant performance impact, so is disabled by default.
  });


  // Sparkline
  var drawSpark = function(){
    $('#spark-bg').sparkline([166,137,187,119,129,124,179,172,138,115,149,195,167,173,152,182,190,139,108,175,170,118,113,122,183,183,120,121,114,141,173], {
      type: 'bar',
      barColor: '#F5F7FA',
      barWidth: '35',
      height: '86',
      disableInteraction: true
    });
    // Items
    $('#spark-items').sparkline([47,40,50,29,27,40,51,50,40,36,28,46,55,48,47,40,31,59,35,53], { type: 'line', fillColor: false, lineColor: '#E6E9ED', width: '90%', height: '42px' });
    $('#spark-items').sparkline([28,25,29,45,42,60,58,30,29,49,25,30,32,48,53,31,65,60,46,35], {
      composite: true, fillColor: false, lineColor: '#AC92EC', width: '90%', height: '42px'
    });
    // Sales
    $('#spark-sales').sparkline([210,330,323,286,316,421,404,427,317,443,328,478,469,315,211,202,228,372,374,503], { type: 'line', fillColor: false, lineColor: '#E6E9ED', width: '90%', height: '42px' });
    $('#spark-sales').sparkline([306,313,525,382,456,502,584,449,447,453,567,512,534,591,469,552,496,455,567,465], {
      composite: true, fillColor: false, lineColor: '#5D9CEC', width: '90%', height: '42px'
    });
    // Sold
    $('#spark-sold').sparkline([144,154,167,183,175,149,199,193,137,120,190,129,125,145,110,196,155,133,200,153], { type: 'line', fillColor: false, lineColor: '#E6E9ED', width: '90%', height: '42px' });
    $('#spark-sold').sparkline([164,186,188,141,150,165,198,150,170,174,162,163,152,181,106,158,180,111,177,135], {
      composite: true, fillColor: false, lineColor: '#48CFAD', width: '90%', height: '42px'
    });
    // Average
    $('#spark-avg').sparkline([39,44,44,30,34,40,65,43,33,54,35,50,59,30,48,45,55,64,34,53], { type: 'line', fillColor: false, lineColor: '#E6E9ED', width: '90%', height: '42px' });
    $('#spark-avg').sparkline([33,44,57,65,51,32,42,45,48,37,54,51,43,31,30,34,55,45,34,35], {
      composite: true, fillColor: false, lineColor: '#FFCE54', width: '90%', height: '42px'
    });
  };

  if (WrapkitUtils.isMobile()) {
    setTimeout(function(){
      graphOpwr.redraw();
      graphSocFol.redraw();
      graphUpdown.redraw();
      drawSpark();
    }, 100);
  } else{
    drawSpark();
  }

  // update when content width changed (only on desktop for save performance)
  if (!WrapkitUtils.isMobile()) {
    [].forEach.call(['show', 'hide', 'size', 'setMode'], function(ev){
      window.sidebar.on( ev, WrapkitUtils.debounce(function(){
        graphOpwr.redraw();
        graphSocFol.redraw();
        graphUpdown.redraw();
        drawSpark();
      }, 250));
    });
    window.wl.on( 'layoutChanged', WrapkitUtils.debounce(function(){
      graphOpwr.redraw();
      graphSocFol.redraw();
      graphUpdown.redraw();
      drawSpark();
    }, 250));
  }
  window.addEventListener( 'resize', WrapkitUtils.debounce(function(){
    drawSpark();
  }, 250));

})(window);