(function(){
  'use strict';

  $('#test-dummy-btn').on( 'click', function(){
    var $target = $('#test-dummy').children(),
    effect = $('#UIPackSelEffect').val(),
    stagger = $('#UIPackSelStagger').val(),
    drag = $('#UIPackSelDrag').val(),
    toastr = window.toastr;

    if (effect) {
      $.Velocity({
        e: $target,
        p: effect,
        o: {
          stagger: stagger,
          drag: drag,
          complete: function(el) {
            setTimeout(function(){
              if ($(el).css('display') === 'none') {
                $.Velocity({ e: el, p: 'transition.fadeIn'});
              }
            }, 600);
          }
        }
      });
    } else{
      toastr.warning( 'Please select an Effect to Test Animtations!' );
    }
  });
})(window);