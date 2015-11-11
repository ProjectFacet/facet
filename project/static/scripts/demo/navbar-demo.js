(function(){
  'use strict';

  var WrapkitPanel = window.WrapkitPanel,
  panelDemo = new WrapkitPanel('#panelNavbarDemo');

  $( '#navbarDemoContext a' ).on( 'click', function(e){
    e.preventDefault();

    var $this = $( this ),
    data = $this.data();

    if (data.navbar === 'default') {
      panelDemo.setContext('dark');
    } else{
      panelDemo.setContext('default');
    }

    $( '#navbar-demo' ).attr( 'class', 'navbar navbar-' + data.navbar );
  });
})(window);