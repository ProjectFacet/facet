(function(){
  'use strict';

  $( document ).on( 'click', '.demo-panel-btn', function(e){
    e.preventDefault();

    var c = 'btn-' + this.dataset.btn;

    $('#demoBtn .btn').removeClass('btn-icon btn-nofill btn-bordered')
    .addClass(c);
  })
  .on( 'change', '#demoFillPanel', function(){
    $('#contextLists a').attr('data-fill', this.checked);
  });
})(window);