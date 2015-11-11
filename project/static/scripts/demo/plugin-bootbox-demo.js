(function(){
  'use strict';

  var bootbox = window.bootbox,
  toastr = window.toastr;

  toastr.options = {
    positionClass: 'toast-top-right',
    progressBar: true
  };

  $( '#bootboxAlert' ).on( 'click', function(){
    bootbox.alert( 'Hello world!', function() {
      toastr.info( 'Hello world callback' );
    });
  });

  $( '#bootboxConfirm' ).on( 'click', function(){
    bootbox.confirm( 'Are you sure?', function( result ) {
      toastr.info( 'Confirm result: ' + result);
    });
  });

  $( '#bootboxPrompt' ).on( 'click', function(){
    bootbox.prompt( 'What is your name?', function( result ) {
      if ( result === null) {
        toastr.warning( 'Prompt dismissed' );
      } else {
        toastr.success( 'Hi <b>' + result + '</b>' );
      }
    });
  });

  $( '#bootboxCustom' ).on( 'click', function(){
    bootbox.dialog({
      message: 'I am a custom dialog',
      title: 'Custom title',
      buttons: {
        success: {
          label: 'Success!',
          className: 'btn-success',
          callback: function() {
            toastr.success('great success');
          }
        },
        danger: {
          label: 'Danger!',
          className: 'btn-danger',
          callback: function() {
            toastr.error('uh oh, look out!');
          }
        },
        main: {
          label: 'Click ME!',
          className: 'btn-primary',
          callback: function() {
            toastr.info('Primary button');
          }
        }
      }
    });
  });
})(window);