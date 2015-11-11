(function(){
  'use strict';

  var updateOutput = function(e){
    var list   = e.length ? e : $(e.target),
    output = list.data('output');
    if (window.JSON) {
      output.val(window.JSON.stringify(list.nestable('serialize')));
    } else {
      output.val('JSON browser support required for this demo.');
    }
  };

  // activate Nestable for list 1
  $( '#nestable' ).nestable({
    group: 1
  })
  .on( 'change', updateOutput );

  // activate Nestable for list 2
  $( '#nestable2' ).nestable({
    group: 1
  }).on( 'change', updateOutput );


  // output initial serialised data
  updateOutput( $( '#nestable' ).data( 'output', $( '#nestable-output') ) );
  updateOutput( $( '#nestable2' ).data( 'output', $( '#nestable2-output') ) );


  $('#nestable3').nestable();


  $('#expand-all').on('click', function(){
    $('.dd').nestable('expandAll');
  });
  $('#collapse-all').on('click', function(){
    $('.dd').nestable('collapseAll');
  });
})(window);