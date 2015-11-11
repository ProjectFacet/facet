(function(){
  'use strict';

  // easyPieChart
  $('.easyPieChart').easyPieChart({
    onStep: function(from, to, currentValue) {
      $(this.el).find('.data-percent').text(currentValue.toFixed(0));
    },
    onStart: function() {
      var canvas = $(this.el).children('canvas'),
      size = canvas.height() + 'px';

      $(this.el).css({
        width: size,
        height: size,
        lineHeight: size
      });
    }
  });

  // update pie chart
  $(document).on('click', '#updatePieCharts', function(e) {
    e.preventDefault();
    $('.easyPieChart').each(function() {
      var val = Math.floor(Math.random() * (80-40+1)) + 40;
      $(this).data('easyPieChart').update( val );
    });
  });
  // end easyPieChart
})(window);