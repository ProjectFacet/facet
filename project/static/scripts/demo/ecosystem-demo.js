(function(){
  'use strict';


  // WRAPKIT LAYOUT DEMO
  document.querySelector('#wlDemoSetFluid').addEventListener( 'click', function(){
    // set to fluid
    window.wl.setFluid();
  });
  document.querySelector('#wlDemoSetBox').addEventListener( 'click', function(){
    // set to box
    window.wl.setBox();
  });
  document.querySelector('#wlDemoFullscreen').addEventListener( 'click', function(){
    // fullscreen mode
    window.wl.fullscreen();
  });
  document.querySelector('#wlDemoExitFullscreen').addEventListener( 'click', function(){
    // exit fullscreen
    window.wl.exitFullscreen();
  });

  // wrapkit layout _events
  // window.wl.on( 'init', function(wl){
  //   console.log(wl);
  // })
  // .on( 'layoutChanged', function(wl, layout){
  //   console.log(layout);
  // })
  // .on( 'fullscreen', function(wl, fs){
  //   console.log(fs);
  // });



  // WRAPKIT HEADER DEMO
  [].forEach.call(document.querySelectorAll('#whDemoSetSkin [data-toggle="header-skin"]'), function(el){
    // set skin
    el.addEventListener( 'click', function(e){
      var skin = el.dataset.skin;
      e.preventDefault();
      window.wh.setSkin( skin );
    });
  });
  document.querySelector('#whDemoFixed').addEventListener( 'click', function(){
    // toggle fixed
    window.wh.fixed(!window.wh.options.fixed);
  });
  document.querySelector('#whDemoFixedTop').addEventListener( 'click', function(){
    // toggle fixed to top
    window.wh.fixedTop();
  });
  document.querySelector('#whDemoFixedBottom').addEventListener( 'click', function(){
    // toggle fixed to bottom
    window.wh.fixedBottom();
  });
  document.querySelector('#whDemoRtlMode').addEventListener( 'click', function(){
    // toggle fixed to bottom
    window.wh.rtl(!window.wh.options.rtlMode);
  });



  // WRAPKIT HEADER DEMO
  document.querySelector('#wcDemoRtlMode').addEventListener( 'click', function(){
    // toggle fixed to bottom
    window.wc.rtl(!window.wc.options.rtlMode);
  });



  // WRAPKIT SIDEBAR DEMO
  [].forEach.call(document.querySelectorAll('#sidebarDemoSkin [data-toggle="sidebar-skin"]'), function(el){
    // set skin
    el.addEventListener( 'click', function(e){
      var skin = el.dataset.skin;
      e.preventDefault();
      window.sidebar.setSkin( skin );
    });
  });
  [].forEach.call(document.querySelectorAll('#sidebarDemoContext [data-toggle="sidebar-context"]'), function(el){
    // set context
    el.addEventListener( 'click', function(e){
      var context = el.dataset.context;
      e.preventDefault();
      window.sidebar.setContext( context );
    });
  });
  [].forEach.call(document.querySelectorAll('[data-toggle="sidebarDemoVariant"]'), function(el){
    // set variant
    el.addEventListener( 'click', function(){
      var variant = el.querySelector('input').value;
      window.sidebar.setVariant( variant );
    });
  });
  document.querySelector('#sidebarDemoVertical').addEventListener( 'click', function(){
    // sidebar vertical
    window.sidebar.setMode('vertical');
  });
  document.querySelector('#sidebarDemoHorizontal').addEventListener( 'click', function(){
    // sidebar horizontal
    window.sidebar.setMode('horizontal');
  });
  document.querySelector('#sidebarDemoFixed').addEventListener( 'click', function(){
    // toggle fixed
    window.sidebar.fixed(!window.sidebar.options.fixed);
  });
  document.querySelector('#sidebarDemoResizeSm').addEventListener( 'click', function(){
    // resize to small
    window.sidebar.size('sm');
  });
  document.querySelector('#sidebarDemoResizeLg').addEventListener( 'click', function(){
    // resize to large
    window.sidebar.size('lg');
  });
  document.querySelector('#sidebarDemoHide').addEventListener( 'click', function(){
    // hide sidebar
    window.sidebar.hide();
  });
  document.querySelector('#sidebarDemoShow').addEventListener( 'click', function(){
    // show sidebar
    window.sidebar.show();
  });
  document.querySelector('#sidebarDemoShowLoader').addEventListener( 'click', function(){
    // show sidebar loader
    window.sidebar.showLoader(3, 'fa-refresh');
  });
  document.querySelector('#sidebarDemoHideLoader').addEventListener( 'click', function(){
    // hide sidebar loader
    window.sidebar.hideLoader(3);
  });
  document.querySelector('#sidebarDemoAlign').addEventListener( 'click', function(){
    // toggle align
    var align = (window.sidebar.options.align === 'left') ? 'right' : 'left';
    window.sidebar.align(align);
  });
  document.querySelector('#sidebarDemoRtl').addEventListener( 'click', function(){
    // toggle direction
    window.sidebar.rtl(!window.sidebar.options.rtlMode);
  });
  document.querySelector('#sidebarDemoResizable').addEventListener( 'click', function(){
    // toggle resizable
    window.sidebar.resizable(!window.sidebar.options.resizable);
  });



  // WRAPKIT SIDEBAR DEMO
  [].forEach.call(document.querySelectorAll('#wfDemoSkin [data-toggle="footer-skin"]'), function(el){
    // set skin
    el.addEventListener( 'click', function(e){
      var skin = el.dataset.skin;
      e.preventDefault();
      window.wf.setSkin( skin );
    });
  });
  document.querySelector('#wfDemoRtl').addEventListener( 'click', function(){
    // toggle direction
    window.wf.rtl(!window.wf.options.rtlMode);
  });
})(window);