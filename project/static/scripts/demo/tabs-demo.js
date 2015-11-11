(function(){
  'use strict';

  $('#demo3-panel').on('setContext', function(e, context){
    var $nav = $('#demo3-tabs');
    if (context === 'dark') {
      $nav.attr('class', 'nav nav-tabs nav-contrast-light');
    } else{
      $nav.attr('class', 'nav nav-tabs nav-contrast-dark');
    }
  });

  // advance usage
  var WrapkitPanel = window.WrapkitPanel,
  demo5Panel = new WrapkitPanel('#demo5-panel');

  $('#demo5-tabs').on('shown.bs.tab', function (e) {
    var current = e.target,
    context = current.dataset.context;

    demo5Panel.setContext(context);
    demo5Panel.setFill(true);
  });
})(window);