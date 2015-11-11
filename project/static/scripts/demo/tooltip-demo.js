(function(){
  'use strict';

  var $tooltipInverse = $('#tooltipInverse');

  $tooltipInverse.on('shown.bs.tooltip', function () {
    $('#panelTooltipDemo').addClass('bg-dark');
  });
  $tooltipInverse.on('hidden.bs.tooltip', function () {
    $('#panelTooltipDemo').removeClass('bg-dark');
  });
})(window);