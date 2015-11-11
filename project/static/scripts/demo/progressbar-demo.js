(function(){
  'use strict';

  $( '#update-progressbar' ).on( 'click', function(){

    var $progress = $( '.progress' );

    $progress.each(function(){
      var progress = $( this ),
      progressBar = progress.children( '.progress-bar' ),
      stacked = ( progressBar.length > 1 ),
      valuenow = Math.floor( Math.random() * ( 100 - 40 + 1 ) + 40 );

      if( stacked ){
        progressBar.each(function(){
          var valuenowStaked = Math.floor( Math.random() * ( 33 - 10 + 1 ) + 10 );
          $( this ).css( 'width', valuenowStaked + '%' )
          .children( '.progress-text' ).text( valuenowStaked + '%' );
        });
      } else{
        progressBar.css( 'width', valuenow + '%' );
        progressBar.children( '.progress-text' ).text( valuenow + '%' );
      }

    });
  });
})(window);