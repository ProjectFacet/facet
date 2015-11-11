(function(){
  'use strict';

  $.sessionTimeout({
    message: 'Your session will be locked in one minute.',
    countdownMessage: 'Redirecting in <span class="label label-warning">{timer}</span> seconds.',
    ignoreUserActivity: true,
    keepAliveUrl: 'keep-alive',
    logoutUrl: 'page-signin.html',
    redirUrl: 'page-locked.html',
    warnAfter: 5000,
    redirAfter: 20000
  });
})(window);