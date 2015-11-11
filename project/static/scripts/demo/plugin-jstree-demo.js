(function(){
  'use strict';

  // jstree1
  $('#jstree1').jstree({
    'core' : {
      'themes': {
        'responsive' : false
      },
      // so that create works
      'check_callback' : true
    },
    'plugins' : [ 'types', 'dnd' ],
    'types' : {
      'default' : {
        'icon' : 'fa fa-folder text-red'
      },
      'file' : {
        'icon' : 'fa fa-file-o'
      },
      'text' : {
        'icon' : 'fa fa-file-text-o'
      },
      'word' : {
        'icon' : 'fa fa-file-word-o'
      },
      'excel' : {
        'icon' : 'fa fa-file-excel-o'
      },
      'ppt' : {
        'icon' : 'fa fa-file-powerpoint-o'
      },
      'pdf' : {
        'icon' : 'fa fa-file-pdf-o'
      },
      'archive' : {
        'icon' : 'fa fa-file-archive-o'
      },
      'image' : {
        'icon' : 'fa fa-file-image-o'
      },
      'audio' : {
        'icon' : 'fa fa-file-audio-o'
      },
      'video' : {
        'icon' : 'fa fa-file-video-o'
      }
    }
  });

  // jstree2
  $('#jstree2').jstree({
    'core' : {
      'themes': {
        'responsive' : false
      },
      // so that create works
      'check_callback' : true
    },
    'plugins' : [ 'types', 'checkbox', 'dnd' ],
    'checkbox' : {
      'keep_selected_style' : false
    },
    'types' : {
      'default' : {
        'icon' : 'fa fa-folder text-blue'
      },
      'file' : {
        'icon' : 'fa fa-file-o text-dark'
      },
      'text' : {
        'icon' : 'fa fa-file-text-o'
      },
      'word' : {
        'icon' : 'fa fa-file-word-o'
      },
      'excel' : {
        'icon' : 'fa fa-file-excel-o'
      },
      'ppt' : {
        'icon' : 'fa fa-file-powerpoint-o'
      },
      'pdf' : {
        'icon' : 'fa fa-file-pdf-o'
      },
      'archive' : {
        'icon' : 'fa fa-file-archive-o'
      },
      'image' : {
        'icon' : 'fa fa-file-image-o'
      },
      'audio' : {
        'icon' : 'fa fa-file-audio-o'
      },
      'video' : {
        'icon' : 'fa fa-file-video-o'
      }
    }
  });


  // jstree3
  $('#jstree3').jstree({
    'core' : {
      'themes': {
        'responsive' : false
      },
      // so that create works
      'check_callback' : true
    },
    'plugins' : [ 'types', 'contextmenu', 'dnd' ],
    'types' : {
      'default' : {
        'icon' : 'fa fa-folder text-teal'
      },
      'file' : {
        'icon' : 'fa fa-file-o'
      },
      'text' : {
        'icon' : 'fa fa-file-text-o'
      },
      'word' : {
        'icon' : 'fa fa-file-word-o'
      },
      'excel' : {
        'icon' : 'fa fa-file-excel-o'
      },
      'ppt' : {
        'icon' : 'fa fa-file-powerpoint-o'
      },
      'pdf' : {
        'icon' : 'fa fa-file-pdf-o'
      },
      'archive' : {
        'icon' : 'fa fa-file-archive-o'
      },
      'image' : {
        'icon' : 'fa fa-file-image-o'
      },
      'audio' : {
        'icon' : 'fa fa-file-audio-o'
      },
      'video' : {
        'icon' : 'fa fa-file-video-o'
      }
    }
  });


  // jstree4
  $('#jstree4').jstree({
    'core' : {
      'themes': {
        'responsive' : false
      },
      // so that create works
      'check_callback' : true
    },
    'plugins' : [ 'types', 'search', 'dnd' ],
    'types' : {
      'default' : {
        'icon' : 'fa fa-folder text-yellow'
      },
      'file' : {
        'icon' : 'fa fa-file-o'
      },
      'text' : {
        'icon' : 'fa fa-file-text-o'
      },
      'word' : {
        'icon' : 'fa fa-file-word-o'
      },
      'excel' : {
        'icon' : 'fa fa-file-excel-o'
      },
      'ppt' : {
        'icon' : 'fa fa-file-powerpoint-o'
      },
      'pdf' : {
        'icon' : 'fa fa-file-pdf-o'
      },
      'archive' : {
        'icon' : 'fa fa-file-archive-o'
      },
      'image' : {
        'icon' : 'fa fa-file-image-o'
      },
      'audio' : {
        'icon' : 'fa fa-file-audio-o'
      },
      'video' : {
        'icon' : 'fa fa-file-video-o'
      }
    }
  });


  var to = false;
  $('#jstree4_q').keyup(function () {
    if(to) {
      clearTimeout(to);
    }
    to = setTimeout(function () {
      var v = $('#jstree4_q').val();
      $('#jstree4').jstree(true).search(v);
    }, 250);
  });
})(window);