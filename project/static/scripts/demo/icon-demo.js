(function(){
  'use strict';

  var demoList = document.querySelectorAll('.demo-icon-list');

  [].forEach.call( demoList, function(el){
    var url = el.dataset.content;
    $(el).load(url);
  });

  $('.demo-icon-container').on('expand', function(e, exp){
    var $liAnim = $(this).find('.demo-icon-list > li:lt(40)'),
    $liWait = $(this).find('.demo-icon-list > li:gt(39)');
    $liWait.css('opacity', 0);

    if (exp) {
      $.Velocity.RunSequence([
        { e: $liAnim, p: 'transition.fadeIn', o: { duration: 150, stagger: 100 } },
        { e: $liWait, p: 'transition.expandIn', o: { duration: 250, stagger: false } }
        ]);
    }
  });
})(window);