(function(){
  'use strict';


  // Panel Tricky: keep body overflow = visible on panel expand
  if ($('.panel[data-expand="true"]').length) {
    document.body.style.overflow = '';
  }
  $('.panel').on( 'expand', function(){
    document.body.style.overflow = '';
  });

  // show hide inbox nav
  $(document).on( 'click', function(){
    $('.inbox-paper').removeClass('open');
  })
  .on( 'click', '#toggle-inbox-nav', function(e){
    e.stopPropagation();
    $('.inbox-paper').toggleClass('open');
  });

})(window);