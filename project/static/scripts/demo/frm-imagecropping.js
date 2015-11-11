(function(){
  'use strict';
  var d = document, ge = 'getElementById', $tabs = $('#jcrop-tabs [data-toggle="tab"]');

  setTimeout(function(){
    $tabs.first().tab('show');
  }, 200);

  // init jcrop after tab shown
  $tabs.on('shown.bs.tab', function(e){
    var tab = $(e.target).data('init');

    if (tab === 'basic') {
      initJcrop1();
    }
    else if(tab === 'thumbnail'){
      initJcrop2();
    }
    else if(tab === 'features'){
      initJcrop3();
    }
    else if(tab === 'styling'){
      initJcrop4();
    }
  });

  var isInitJcrop1 = false,
  isInitJcrop2 = false,
  isInitJcrop3 = false,
  isInitJcrop4 = false;

  // basic
  function initJcrop1(){

    if (isInitJcrop1) { return; }

    $('#jcrop1').Jcrop({
      setSelect: [ 200, 100, 200, 200 ]
    });
    $('#jcrop1-container').on('cropmove cropend',function(e,s,c){
      d[ge]('crop-x').value = c.x;
      d[ge]('crop-y').value = c.y;
      d[ge]('crop-w').value = c.w;
      d[ge]('crop-h').value = c.h;
    });
    // update form fields
    $('#text-inputs').on('change','input',function(){
      $('#jcrop1').Jcrop('api').animateTo([
        parseInt(d[ge]('crop-x').value),
        parseInt(d[ge]('crop-y').value),
        parseInt(d[ge]('crop-w').value),
        parseInt(d[ge]('crop-h').value)
        ]);
    });

    isInitJcrop1 = true;
  }

  // Thumbnail
  // Create a scope-wide variable to hold the Thumbnailer instance
  var thumbnail;
  function initJcrop2(){

    if (isInitJcrop2){ return; }

    // Instantiate Jcrop
    $('#jcrop2').Jcrop({
      aspectRatio: 1,
      setSelect: [ 200, 100, 200, 200 ]
    },function(){
      thumbnail = this.initComponent('Thumbnailer', { width: 130, height: 130 });
      thumbnail.element.css({
        bottom: 0,
        right: 0
      }).parent().css('position', 'relative');
    });

    // Wire up the auto-hide checkbox/toggle
    $('#autohide').attr('checked',false).on('change',function(){
      var chk = this.checked;
      if (thumbnail) {
        thumbnail.autoHide = chk? true: false;
        thumbnail[chk?'hide':'show']();
      }
    });

    isInitJcrop2 = true;
  }


  // Features
  function initJcrop3(){

    if (isInitJcrop3) { return; }

    var $targ = $('#jcrop3');

    $targ.Jcrop({
      animEasing: 'linear',
      bgOpacity: 0.35,
      linked: false,
      multi: true
    },function(){
      this.container.addClass('jcrop-dark jcrop-hl-active');
      interfaceLoad(this);
    });

    function interfaceLoad(obj){
      var cb = obj;

      cb.newSelection();
      cb.setSelect([ 200, 100, 200, 200 ]);
      cb.refresh();
      // Hack a "special" selection...
      var logosel = cb.newSelection().update($.Jcrop.wrapFromXywh([73,268,400,100]));

      $.extend(logosel,{
        special: true, // custom value used in our local script here
        bgColor: '#999',
        bgOpacity: 0.8,
        canResize: false,
        canDelete: false
      });

      logosel.element.prepend('<img src="images/favicons/android-chrome-192x192.png" style="position:absolute;background-color:white;width:100%;height:100%;" />');
      logosel.aspectRatio = 1;
      logosel.refresh();
      cb.ui.multi[1].focus();

      $('#filter-selections input').attr('checked',false);
      $('#page-interface').on('startselect',function(e){
        e.preventDefault();
      });

      /**
       *
       */
       cb.container.on('cropfocus cropblur cropstart cropend',function(e){
        var sel = $(e.target).data('selection');
        switch(e.type){
          case 'cropfocus':
          $('#can_size')[0].checked = sel.canResize?true:false;
          $('#can_delete')[0].checked = sel.canDelete?true:false;
          $('#can_drag')[0].checked = sel.canDrag?true:false;
          $('#set_minsize')[0].checked = (sel.minSize[0]>8)?true:false;
          $('#set_maxsize')[0].checked = (sel.maxSize[0])?true:false;
          $('#set_bounds')[0].checked = (sel.edge.n)?true:false;
          $('#is_linked')[0].disabled = sel.special?true:false;
          $('#is_linked')[0].checked = sel.linked?true:false;
          $('#shading-tools a')[0].disabled = sel.special?true:false;
          $('#shading-tools a')[sel.special?'addClass':'removeClass']('disabled');

          $('#ar-links').find('.active').removeClass('active');
          if (sel.aspectRatio) {
            if (!$('#ar-links').find('[data-value="'+sel.aspectRatio+'"]').addClass('active').length){
              $('#ar-lock').addClass('active');
            }
          } else {
            $('#ar-free').addClass('active');
          }
        }
      });

$('#is_linked').on('change',function(e){
  cb.ui.selection.linked = e.target.checked;
});

$('#selection-options').on('change','[data-filter-toggle]',function(e){
  var tog = $(e.target).data('filter-toggle');
  var o = { };
  o[tog] = e.target.checked? true: false;
  cb.setOptions(o);
});

var cycleColors = [
'red',
'blue',
'gray',
'yellow',
'orange',
'green',
'white'
];

function randomCoords() {
  return [
  Math.random()*300,
  Math.random()*200,
  (Math.random()*540)+50,
  (Math.random()*340)+60
  ];
}

$('#can_drag,#can_size,#can_delete,#enablesel,#multisel,#anim_mode').attr('checked','checked');
$('#is_linked').attr('checked',false);

function animMode(){
  return document.getElementById('anim_mode').checked;
}

      // A simple function to cleanup multiple spawned selections
      function runCleanup(){
        var m = cb.ui.multi, s = cb.ui.selection;

        for(var i=0;i<m.length;i++){
          if (s !== m[i]){
            m[i].remove();
          }
        }

        cb.ui.multi = [ s ];
        s.center();
        s.focus();
      }

      // Animate button event
      $(document.body).on('click','[data-action]',function(e){
        var $targ = $(e.target);
        var action = $targ.data('action');

        switch(action){
          case 'set-maxsize':
          cb.setOptions({ maxSize: e.target.checked? [300,200]: [0,0] });
          break;
          case 'set-minsize':
          cb.setOptions({ minSize: e.target.checked? [60,60]: [8,8] });
          break;
          case 'set-bounds':
          if (e.target.checked){
            cb.setOptions({ edge: {
              n: 15,
              e: -20,
              s: -40,
              w: 28
            }});
          }
          else {
            cb.setOptions({ edge: {
              n: 0,
              e: 0,
              s: 0,
              w: 0
            }});
          }
          break;
          case 'set-ar':
          var value = $targ.data('value');
          $targ.closest('#ar-links').find('.active').removeClass('active');
          if (value === 'lock'){
            var b = cb.ui.selection.get();
            value = b.w / b.h;
          }
          $targ.addClass('active');
          cb.setOptions({ aspectRatio: value });
          break;
          case 'set-selmode':
          $targ.closest('.btn-group').find('.active').removeClass('active');
          $targ.addClass('active');
          switch($targ.data('mode')){
            case 'none':
            cb.container.addClass('jcrop-nodrag');
            cb.setOptions({ allowSelect: false });
            break;
            case 'single':
            cb.container.removeClass('jcrop-nodrag');
            cb.setOptions({ allowSelect: true, multi: false });
            break;
            case 'multi':
            cb.container.removeClass('jcrop-nodrag');
            cb.setOptions({ allowSelect: true, multi: true });
            break;
          }
          break;
          case 'enable-selections':
          cb.ui.stage.dragger.active = e.target.checked;
          break;
          case 'enable-multi':
          cb.ui.stage.dragger.multi = e.target.checked;
          break;
          case 'color-cycle':
          var cc = cycleColors.shift();
          cb.setOptions({ bgColor: cc });
          cycleColors.push(cc);
          break;
          case 'set-opacity':
          $targ.closest('.btn-group').find('.active').removeClass('active');
          $targ.addClass('active');
          cb.setOptions({ bgOpacity: $targ.data('opacity'), bgColor: 'black' });
          break;
          case 'cleanup-all':
          runCleanup();
          break;
          case 'random-move':
          cb[animMode()?'animateTo':'setSelect'](randomCoords());
          break;
        }

      }).on('keydown',function(e){
        if (e.keyCode === 8) {
          e.preventDefault();
        }
      }).on('selectstart',function(e){
        e.preventDefault();
      }).on('click','a[data-action]',function(e){
        e.preventDefault();
      });
    }

    isInitJcrop3 = true;
  }


  // styling
  function initJcrop4(){

    if (isInitJcrop4) { return; }

    // Create a new Selection object extended from Selection
    var CircleSel = function(){ }, jcrop4 = $('#jcrop4'), cb;

    // Set the custom selection's prototype object to be an instance
    // of the built-in Selection object
    CircleSel.prototype = new $.Jcrop.component.Selection();

    // Then we can continue extending it
    $.extend(CircleSel.prototype,{
      zoomscale: 1,
      attach: function(){
        this.frame.css({
          background: 'url(' + jcrop4[0].src + ')'
        });
      },
      positionBg: function(b){
        // var midx = ( b.x + b.x2 ) / 2;
        // var midy = ( b.y + b.y2 ) / 2;
        // var ox = (-midx*this.zoomscale)+(b.w/2);
        // var oy = (-midy*this.zoomscale)+(b.h/2);
        //this.frame.css({ backgroundPosition: ox+'px '+oy+'px' });
        this.frame.css({ backgroundPosition: -(b.x+1)+'px '+(-b.y-1)+'px' });
      },
      redraw: function(b){

        // Call original update() method first, with arguments
        $.Jcrop.component.Selection.prototype.redraw.call(this,b);

        this.positionBg(this.last);
        return this;
      },
      prototype: $.Jcrop.component.Selection.prototype
    });

    // Jcrop Initialization
    jcrop4.Jcrop({

      // Change default Selection component for new selections
      selectionComponent: CircleSel,

      // Use a default filter chain that omits shader
      applyFilters: [ 'constrain', 'extent', 'backoff', 'ratio', 'round' ],

      // Start with circles only
      aspectRatio: 1,

      // Set an initial selection
      setSelect: [ 200, 100, 200, 200 ],

      // Only n/s/e/w handles
      handles: [ 'n','s','e','w' ],

      // No dragbars or borders
      dragbars: [ ],
      borders: [ ]

    },function(){
      this.container.addClass('jcrop-circle');
      interfaceLoad(this);
    });

    function interfaceLoad(obj){
      cb = obj;

      // Add in a custom shading element...
      cb.container.prepend($('<div />').addClass('circle-shade'));

      function randomCoords() {
        return [
        Math.random()*300,
        Math.random()*200,
        (Math.random()*540)+50,
        (Math.random()*340)+60
        ];
      }

      // Settings Buttons
      $(document.body).on('click','[data-setting]',function(e){
        var $targ = $(e.target),
        setting = $targ.data('setting'),
        value = $targ.data('value'),
        opt = {};

        opt[setting] = value;
        cb.setOptions(opt);

        $targ.closest('.btn-group').find('.active').removeClass('active');
        $targ.addClass('active');

        if ((setting === 'multi') && !value) {
          var m = cb.ui.multi, s = cb.ui.selection;

          for(var i=0;i<m.length;i++){
            if (s !== m[i]){
              m[i].remove();
            }
          }

          cb.ui.multi = [ s ];
          s.focus();
        }

        e.preventDefault();
      });

      // Animate button event
      $(document.body).on('click','[data-action]',function(e){
        var $targ = $(e.target);
        var action = $targ.data('action');

        switch(action){
          case 'random-move':
          cb.ui.selection.animateTo(randomCoords());
          break;
        }

        cb.ui.selection.refresh();

      }).on('selectstart',function(e){
        e.preventDefault();
      }).on('click','a[data-action]',function(e){
        e.preventDefault();
      });
    }

    isInitJcrop4 = true;
  }
})(window);