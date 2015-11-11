(function(){
  'use strict';

  var Morris = window.Morris,
  WrapkitUtils = window.WrapkitUtils;

  var morrisArea = Morris.Area({
    element: 'hero-area',
    fillOpacity: 1,
    lineWidth: 0,
    data: [
      {period: '2013 Q1', iphone: 2666, ipad: null, itouch: 2647},
      {period: '2013 Q2', iphone: 2778, ipad: 2294, itouch: 2441},
      {period: '2013 Q3', iphone: 4912, ipad: 1969, itouch: 2501},
      {period: '2013 Q4', iphone: 3767, ipad: 3597, itouch: 5689},
      {period: '2014 Q1', iphone: 6810, ipad: 1914, itouch: 2293},
      {period: '2014 Q2', iphone: 5670, ipad: 4293, itouch: 1881},
      {period: '2014 Q3', iphone: 4820, ipad: 3795, itouch: 1588},
      {period: '2014 Q4', iphone: 15073, ipad: 5967, itouch: 5175},
      {period: '2015 Q1', iphone: 10687, ipad: 4460, itouch: 2028},
      {period: '2015 Q2', iphone: 8432, ipad: 5713, itouch: 1791}
    ],
    xkey: 'period',
    ykeys: ['iphone', 'ipad', 'itouch'],
    labels: ['iPhone', 'iPad', 'iPod Touch'],
    pointSize: 0,
    hideHover: true,
    lineColors: ['#48CFAD', '#A0D468', '#FFCE54'],
    gridTextColor: 'rgba(22, 24, 27, 0.87)',
    gridLineColor: 'rgba(22, 24, 27, 0.26)',
    resize: true // NOTE: This has a significant performance impact, so is disabled by default.
  });

  // data stolen from http://howmanyleft.co.uk/vehicle/jaguar_'e'_type
  var taxData = [
    {'period': '2011 Q3', 'licensed': 3407, 'sorned': 660},
    {'period': '2011 Q2', 'licensed': 3351, 'sorned': 629},
    {'period': '2011 Q1', 'licensed': 3269, 'sorned': 618},
    {'period': '2010 Q4', 'licensed': 3246, 'sorned': 661},
    {'period': '2009 Q4', 'licensed': 3171, 'sorned': 676},
    {'period': '2008 Q4', 'licensed': 3155, 'sorned': 681},
    {'period': '2007 Q4', 'licensed': 3226, 'sorned': 620},
    {'period': '2006 Q4', 'licensed': 3245, 'sorned': null},
    {'period': '2005 Q4', 'licensed': 3289, 'sorned': null}
  ];
  var morrisLine = Morris.Line({
    element: 'hero-graph',
    data: taxData,
    xkey: 'period',
    ykeys: ['licensed', 'sorned'],
    labels: ['Licensed', 'Off the road'],
    lineColors: [ '#5D9CEC', '#48CFAD' ],
    gridTextColor: 'rgba(22, 24, 27, 0.87)',
    gridLineColor: 'rgba(22, 24, 27, 0.26)',
    resize: true // NOTE: This has a significant performance impact, so is disabled by default.
  });

  var morrisBar = Morris.Bar({
    element: 'hero-bar',
    data: [
      {device: 'iPhone', geekbench: 136},
      {device: 'iPhone 3G', geekbench: 137},
      {device: 'iPhone 3GS', geekbench: 275},
      {device: 'iPhone 4', geekbench: 380},
      {device: 'iPhone 4S', geekbench: 655},
      {device: 'iPhone 5', geekbench: 1571}
    ],
    xkey: 'device',
    ykeys: ['geekbench'],
    labels: ['Geekbench'],
    barRatio: 0.4,
    xLabelAngle: 35,
    hideHover: 'auto',
    barColors: ['#5D9CEC'],
    gridTextColor: 'rgba(22, 24, 27, 0.87)',
    gridLineColor: 'rgba(22, 24, 27, 0.26)',
    resize: true // NOTE: This has a significant performance impact, so is disabled by default.
  });


  // Donut
  var morrisDonut1 = Morris.Donut({
    element: 'hero-donut',
    data: [
      {label: 'Week 1', value: 21 },
      {label: 'Week 2', value: 33 },
      {label: 'Week 3', value: 45 },
      {label: 'Week 4', value: 12 }
    ],
    labelColor: '#5D9CEC',
    formatter: function (y) { return y + '%'; },
    colors: [ '#5D9CEC', '#7FB0F0', '#A4C7F4', '#C8DDF9' ],
    resize: true
  });
  var morrisDonut2 = Morris.Donut({
    element: 'hero-donut2',
    data: [
      {label: 'Week 1', value: 75 },
      {label: 'Week 2', value: 32 },
      {label: 'Week 3', value: 68 },
      {label: 'Week 4', value: 40 }
    ],
    labelColor: '#ED5565',
    formatter: function (y) { return y + '%'; },
    colors: [ '#ED5565', '#F17E89', '#F5A3AB', '#F9C8CD' ],
    resize: true
  });
  var morrisDonut3 = Morris.Donut({
    element: 'hero-donut3',
    data: [
      {label: 'Week 1', value: 54 },
      {label: 'Week 2', value: 95 },
      {label: 'Week 3', value: 42 },
      {label: 'Week 4', value: 67 }
    ],
    labelColor: '#48CFAD',
    formatter: function (y) { return y + '%'; },
    colors: [ '#48CFAD', '#6ED8BE', '#8EE1CC', '#AEEADB' ],
    resize: true
  });

  // update when content width changed (only on desktop for save performance)
  if (!WrapkitUtils.isMobile()) {
    [].forEach.call(['show', 'hide', 'size', 'setMode'], function(ev){
      window.sidebar.on( ev, WrapkitUtils.debounce(function(){
        morrisArea.redraw();
        morrisLine.redraw();
        morrisBar.redraw();
        morrisDonut1.redraw();
        morrisDonut2.redraw();
        morrisDonut3.redraw();
      }, 250));
    });
    window.wl.on( 'layoutChanged', WrapkitUtils.debounce(function(){
      morrisArea.redraw();
      morrisLine.redraw();
      morrisBar.redraw();
      morrisDonut1.redraw();
      morrisDonut2.redraw();
      morrisDonut3.redraw();
    }, 250));
  }
})(window);