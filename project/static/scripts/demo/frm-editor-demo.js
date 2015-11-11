(function(){
  'use strict';

  var EpicEditor = window.EpicEditor,
  WrapkitUtils = window.WrapkitUtils;

  // summernote
  $('#summernote').summernote({
    height: 300,
    fontNames: ['Open Sans', 'Arial', 'Arial Black', 'Comic Sans MS', 'Courier New', 'Helvetica', 'Immpact', 'Tahoma', 'Times New Roman', 'Verdana'],
    fontNamesIgnoreCheck: ['Open Sans'],
    toolbar: [
    ['style', ['style']],
    ['font', ['bold', 'italic', 'underline', 'clear']],
    ['fontname', ['fontname']],
    ['fontsize', ['fontsize']], // Still buggy
    ['color', ['color']],
    ['para', ['ul', 'ol', 'paragraph']],
    ['height', ['height']],
    ['table', ['table']],
    ['insert', ['link', 'picture', 'video']],
    ['view', ['fullscreen', 'codeview']],
    ['help', ['help']]
    ]
  });



  // epiceditor
  var opts = {
    container: 'epiceditor',      // container id
    textarea: 'epiceditor-edit-area', // textarea id
    basePath: '',           // bash path to take source
    theme: {
      base: 'styles/epiceditor/base/epiceditor.css',
      preview: 'styles/bootstrap.css',
      editor: 'styles/epiceditor/editor/epic-dark.css'
    },
    autogrow: {
      minHeight: 500,
      maxHeight: 500
    }
  },
  epicEditor = new EpicEditor( opts ).load();

  // Change fullscreen
  $( '#epicFull' ).on( 'click', function(e){
    e.preventDefault();

    if (! epicEditor.is('loaded') ) { return; }
    epicEditor.enterFullscreen();
  });

  // get content
  $( '#epiceditorGetText' ).on( 'click', function(){
    var text = $( '#epiceditor-edit-area' ).val();  // Returns the editor's text

    $( '#markdown-result' ).val( text );
  });
  $( '#epiceditorGetHtml' ).on( 'click', function(){
    var previewer = epicEditor.getElement('previewer').body,
      html = $( previewer ).children('div').html(); // Returns the editor's html

      $( '#markdown-result' ).val( html );
    });


  // epicEditor2
  var opts2 = {
    container: 'epiceditor2',     // container id
    textarea: 'epiceditor-edit-area2',  // textarea id
    basePath: '',           // bash path to take source
    theme: {
      base: 'styles/epiceditor/base/epiceditor.css',
      preview: 'styles/epiceditor/preview/github.css',
      editor: 'styles/epiceditor/editor/epic-light.css'
    },
    autogrow: {
      minHeight: 500,
      maxHeight: 500
    }
  },
  epicEditor2 = new EpicEditor( opts2 ).load();

  // Change fullscreen
  $( '#epicFull2' ).on( 'click', function(e){
    e.preventDefault();

    if (! epicEditor2.is('loaded') ) { return; }
    epicEditor2.enterFullscreen();
  });
  
  // get content
  $( '#epiceditorGetText2' ).on( 'click', function(){
    var text = $( '#epiceditor-edit-area2' ).val(); // Returns the editor's text

    $( '#markdown-result' ).val( text );
  });
  $( '#epiceditorGetHtml2' ).on( 'click', function(){
    var previewer = epicEditor2.getElement('previewer').body,
      html = $( previewer ).children('div').html(); // Returns the editor's html

      $( '#markdown-result' ).val( html );
    });


  // responsive support
  window.onresize = WrapkitUtils.debounce(function(){
    epicEditor.reflow();
    epicEditor2.reflow();
  }, 200);
  [].forEach.call(['show', 'hide', 'size'], function(ev){
    window.sidebar.on( ev, WrapkitUtils.debounce(function(){
      epicEditor.reflow();
      epicEditor2.reflow();
    }, 250));
  });


  // select result
  $( '#select-result' ).on( 'click', function(e){
    e.preventDefault();
    $( '#markdown-result' ).select();
  });
})(window);