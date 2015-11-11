(function(){
  'use strict';

  // sidebar vertical
  document.querySelector('#btn-sd-vertical')
  .addEventListener( 'click', function(){
    window.sidebar.setMode('vertical');
  });
  // sidebar horizontal
  document.querySelector('#btn-sd-horizontal')
  .addEventListener( 'click', function(){
    window.sidebar.setMode('horizontal');
  });
  // sidebar small
  document.querySelector('#btn-sd-small')
  .addEventListener( 'click', function(){
    window.sidebar.size('sm');
  });
  // sidebar large
  document.querySelector('#btn-sd-large')
  .addEventListener( 'click', function(){
    window.sidebar.size('lg');
  });
  // hide/show sidebar
  document.querySelector('#btn-sd-toggle')
  .addEventListener( 'click', function(){
    if (window.sidebar.options.visible) {
      window.sidebar.hide();
    } else{
      window.sidebar.show();
    }
  });
  // sidebar right
  document.querySelector('#btn-sd-right')
  .addEventListener( 'click', function(){
    window.sidebar.align('right');
  });
  // sidebar left
  document.querySelector('#btn-sd-left')
  .addEventListener( 'click', function(){
    window.sidebar.align('left');
  });
  // rtl direction
  var rtl = false;
  document.querySelector('#btn-sd-rtl')
  .addEventListener( 'click', function(){
    if (rtl) {
      window.wh.rtl(false);
      window.wc.rtl(false);
      window.sidebar.rtl(false);
      window.wf.rtl(false);
    } else{
      window.wh.rtl(true);
      window.wc.rtl(true);
      window.sidebar.rtl(true);
      window.wf.rtl(true);
    }
    rtl = (!rtl);
  });
  // header fixed
  document.querySelector('#btn-hd-fixed')
  .addEventListener( 'click', function(){
    window.wh.fixed(true);
    window.sidebar.fixed(false);
  });
  // sidebar fixed
  document.querySelector('#btn-sd-fixed')
  .addEventListener( 'click', function(){
    window.wh.fixed(false);
    window.sidebar.fixed(true);
  });
  // fixed all
  document.querySelector('#btn-hsd-fixed')
  .addEventListener( 'click', function(){
    window.wh.fixed(true);
    window.sidebar.fixed(true);
  });
  // nofixed
  document.querySelector('#btn-hsd-nofixed')
  .addEventListener( 'click', function(){
    window.wh.fixed(false);
    window.sidebar.fixed(false);
  });

})(window);