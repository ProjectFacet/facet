(function(){
  'use strict';

  var toastr = window.toastr,
  i = -1,
  toastCount = 0,
  $toastlast,
  getMessage = function () {
    var msgs = ['Hi! My name is Inigo Montoya.',
    'Are you the six fingered man?',
    'Inconceivable!',
    'I do not think that means what you think it means.',
    'Have fun storming the castle!'
    ];
    i++;
    if (i === msgs.length) {
      i = 0;
    }

    return msgs[i];
  };


  $('#showtoast').click(function () {
    var shortCutFunction = $('#toastTypeGroup input:radio:checked').val();
    var msg = $('#message').val();
    var title = $('#title').val() || '';
    var $showDuration = $('#showDuration');
    var $hideDuration = $('#hideDuration');
    var $timeOut = $('#timeOut');
    var $extendedTimeOut = $('#extendedTimeOut');
    var $showEasing = $('#showEasing');
    var $hideEasing = $('#hideEasing');
    var $showMethod = $('#showMethod');
    var $hideMethod = $('#hideMethod');
    var toastIndex = toastCount++;

    toastr.options = {
      closeButton: $('#closeButton').prop('checked'),
      debug: $('#debugInfo').prop('checked'),
      newestOnTop: $('#newestOnTop').prop('checked'),
      progressBar: $('#progressBar').prop('checked'),
      positionClass: $('#positionGroup input:radio:checked').val() || 'toast-top-right',
      preventDuplicates: $('#preventDuplicates').prop('checked'),
      onclick: null
    };

    if ($('#addBehaviorOnToastClick').prop('checked')) {
      toastr.options.onclick = function () {
        window.alert('You can perform some custom action after a toast goes away');
      };
    }

    if ($showDuration.val().length) {
      toastr.options.showDuration = $showDuration.val();
    }

    if ($hideDuration.val().length) {
      toastr.options.hideDuration = $hideDuration.val();
    }

    if ($timeOut.val().length) {
      toastr.options.timeOut = $timeOut.val();
    }

    if ($extendedTimeOut.val().length) {
      toastr.options.extendedTimeOut = $extendedTimeOut.val();
    }

    if ($showEasing.val().length) {
      toastr.options.showEasing = $showEasing.val();
    }

    if ($hideEasing.val().length) {
      toastr.options.hideEasing = $hideEasing.val();
    }

    if ($showMethod.val().length) {
      toastr.options.showMethod = $showMethod.val();
    }

    if ($hideMethod.val().length) {
      toastr.options.hideMethod = $hideMethod.val();
    }

    if (!msg) {
      msg = getMessage();
    }

    $('#toastrOptions').text('Command: toastr[' +
      shortCutFunction +
      '](\'' +
        msg +
        (title ? '\', \'' + title : '') +
        '\')\n\ntoastr.options = ' +
    JSON.stringify(toastr.options, null, 2)
    );

    var $toast = toastr[shortCutFunction](msg, title); // Wire up an event handler to a button in the toast, if it exists
    $toastlast = $toast;
    if ($toast.find('#okBtn').length) {
      $toast.delegate('#okBtn', 'click', function () {
        window.alert('you clicked me. i was toast #' + toastIndex + '. goodbye!');
        $toast.remove();
      });
    }
    if ($toast.find('#surpriseBtn').length) {
      $toast.delegate('#surpriseBtn', 'click', function () {
        window.alert('Surprise! you clicked me. i was toast #' + toastIndex + '. You could perform an action here.');
      });
    }
    if ($toast.find('.clear').length) {
      $toast.delegate('.clear', 'click', function () {
        toastr.clear($toast, { force: true });
      });
    }
  });

  // getlast
  function getLastToast(){
    return $toastlast;
  }
  $('#clearlasttoast').click(function () {
    toastr.clear(getLastToast());
  });
  $('#cleartoasts').click(function () {
    toastr.clear();
  });

})(window);