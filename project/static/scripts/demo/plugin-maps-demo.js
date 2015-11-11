(function(){
  'use strict';

  // on panel #1
  $('#vmap1').vectorMap({
    map: 'asia_en',
    backgroundColor: null,
    hoverOpacity: 0.9,
    color: '#ED5565',
    selectedColor: '#ED5565',
    enableZoom: false,
    showTooltip: true
  });
  $('#vmap2').vectorMap({
    map: 'europe_en',
    backgroundColor: null,
    hoverOpacity: 0.9,
    color: '#48CFAD',
    selectedColor: '#48CFAD',
    enableZoom: false,
    showTooltip: true
  });
  $('#vmap3').vectorMap({
    map: 'north-america_en',
    backgroundColor: null,
    hoverOpacity: 0.9,
    color: '#4FC1E9',
    selectedColor: '#4FC1E9',
    enableZoom: false,
    showTooltip: true
  });

  // on panel #2
  $('#vmap4').vectorMap({
    map: 'world_en',
    backgroundColor: null,
    color: '#F5F7FA',
    selectedColor: '#434A54',
    hoverOpacity: 0.7,
    enableZoom: true,
    showTooltip: true,
    scaleColors: ['#E6E9ED', '#CCD1D9'],
    normalizeFunction: 'polynomial'
  });

  $('#vmap4').vectorMap('set', 'colors', {us: '#ED5565'});
  $('#vmap4').vectorMap('set', 'colors', {ru: '#FFCE54'});
  $('#vmap4').vectorMap('set', 'colors', {id: '#48CFAD'});
  $('#vmap4').vectorMap('set', 'colors', {br: '#5D9CEC'});
  $('#vmap4').vectorMap('set', 'colors', {gb: '#AC92EC'});

  // on panel #3
  $('#vmap5').vectorMap({
    map: 'africa_en',
    backgroundColor: null,
    hoverOpacity: 0.7,
    color: '#48CFAD',
    selectedColor: '#48CFAD',
    enableZoom: false,
    showTooltip: true
  });
  $('#vmap6').vectorMap({
    map: 'asia_en',
    backgroundColor: null,
    hoverOpacity: 0.7,
    color: '#48CFAD',
    selectedColor: '#48CFAD',
    enableZoom: false,
    showTooltip: true
  });
  $('#vmap7').vectorMap({
    map: 'europe_en',
    backgroundColor: null,
    hoverOpacity: 0.7,
    color: '#48CFAD',
    selectedColor: '#48CFAD',
    enableZoom: false,
    showTooltip: true
  });
  $('#vmap8').vectorMap({
    map: 'north-america_en',
    backgroundColor: null,
    hoverOpacity: 0.7,
    color: '#48CFAD',
    selectedColor: '#48CFAD',
    enableZoom: false,
    showTooltip: true
  });
})(window);