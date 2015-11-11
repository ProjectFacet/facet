(function(){
  'use strict';

  // custom default setting datatables
  $.extend( true, $.fn.dataTable.defaults, {
    'autoWidth': false, // disabled smart width
    'language': {
      'lengthMenu': '_MENU_ records',
      'search': ''
    }
  });

  var datatables1 = $( '#datatables1' ).dataTable({
    'sDom': 'rt<"table-footer"<"pull-left"i>p>',
    'oLanguage': {
      'sInfoFiltered': '<span class="label label-info"><i class="fa fa-filter"></i> filtering from _MAX_ records</span>',
    },
    'sAjaxSource': '_includes/data-source.json',
    'fnInitComplete': function(settings) {
      var aoData = settings.aoData;

      // adding uniquen id to TR to crud
      $.each( aoData, function(i, val){
        var $ntr = $( val.nTr );

        $ntr.attr( 'data-id', 'datatables1_' + i );
      });

      var $nTable = $(settings.nTable);
      $nTable.closest( '.dataTables_wrapper' ).find( '.dataTable' ).wrap('<div class="table-responsive"></div>');
    },
    'drawCallback': function( settings ) {
      var $nTable = $(settings.nTable);
      $nTable.closest( '.dataTables_wrapper' ).find( '.dataTables_paginate' ).children( '.pagination' )
      .addClass( 'pagination-circle' );
    }
  });

  // simple validate to form add and edit datatables1
  $('#formAddDatatables1').validate({
    errorElement: 'small',
    errorClass: 'help-block text-danger',
    errorPlacement: function(error, element) {
      var $errorPlacement = $(element).parent();

      if ( $(element).is( 'select' ) ) {
        $errorPlacement = $errorPlacement.parent();
      }
      error.appendTo( $errorPlacement );
    },
    highlight: function(element){
      var $errorContainer = $(element).parent();

      if ( $(element).is( 'select' ) ) {
        $errorContainer.parent().addClass( 'has-error' );
      } else{
        $errorContainer.addClass( 'has-error' );
      }
    },
    unhighlight: function(element){
      var $errorContainer = $(element).parent();

      if ( $(element).is( 'select' ) ) {
        $errorContainer.parent().removeClass( 'has-error' );
      } else{
        $errorContainer.removeClass( 'has-error' );
      }
    }
  });

  $('#formEditDatatables1').validate({
    errorElement: 'small',
    errorClass: 'help-block text-danger',
    errorPlacement: function(error, element) {
      var $errorPlacement = $(element).parent();

      if ( $(element).is( 'select' ) ) {
        $errorPlacement = $errorPlacement.parent();
      }
      error.appendTo( $errorPlacement );
    },
    highlight: function(element){
      var $errorContainer = $(element).parent();

      if ( $(element).is( 'select' ) ) {
        $errorContainer.parent().addClass( 'has-error' );
      } else{
        $errorContainer.addClass( 'has-error' );
      }
    },
    unhighlight: function(element){
      var $errorContainer = $(element).parent();

      if ( $(element).is( 'select' ) ) {
        $errorContainer.parent().removeClass( 'has-error' );
      } else{
        $errorContainer.removeClass( 'has-error' );
      }
    }
  });

  // custom filtering
  $( '#filterDatatables1' ).on( 'keyup', function(){
    var value = $( this ).val();

    datatables1.fnFilter( value );
  });

  // selectable datatables ( control with single or multiple select )
  $( document ).on( 'change', '#allowMultipleSelect', function(){
    // remove all selected row
    datatables1.$( 'tr.active' ).removeClass( 'active' );
    // disable actions edit & delete
    $( '.datatables1-actions' ).addClass( 'disabled' );
  })
  // selectable rule
  .on( 'click', '#datatables1 tbody tr', function(){
    var $tr = $( this ),
    allowMultipleSelect = $( '#allowMultipleSelect' ).is(':checked');

    if ( allowMultipleSelect ) {  // multiple select
      $tr.toggleClass( 'active' );
    }
    else{ // single select
      if ( $tr.hasClass( 'active' ) ) {
        $tr.removeClass( 'active' );
      }
      else {
        datatables1.$( 'tr.active' ).removeClass( 'active' );
        $tr.addClass( 'active' );
      }
    }

    // control the event buttons
    var selected = datatables1.$( 'tr.active' ).length;

    if ( selected > 1 ) {
      $( '.datatables1-actions' ).addClass( 'disabled' );
      $( '#delete-datatables1' ).removeClass( 'disabled' );
    }
    else if( selected === 1 ){
      $( '.datatables1-actions' ).removeClass( 'disabled' );
    }
    else{
      $( '.datatables1-actions' ).addClass( 'disabled' );
      // hide form edit
      $( '#editFormContainer' ).addClass( 'hide' );
    }

    // control form edit
    // get data from selected row
    getDataSelected();
  });

  // delete rule
  $( document ).on( 'click', '#delete-datatables1', function(e){
    var dataSelected = datatables1.$( 'tr.active' ),
    deleteCount = dataSelected.length, deletes;

    if (deleteCount) {
      window.bootbox.confirm( 'Are you sure want to delete(s) this data?', function(result){
        deletes = result;

        if( deletes ){

          if ( deleteCount !== 0 ) {

            // process it one by one
            dataSelected.each( function( i, $elem ){

              // do server action here ( ajax )
              // ...

              // deleting selected data
              datatables1.fnDeleteRow( $elem );
            });
          }
          // disabled button
          $( '.datatables1-actions' ).addClass( 'disabled' );
        }
      });
    } else{
      e.preventDefault();
      return;
    }
  })
  // add rule
  .on( 'click', '#add-datatables1, #hideAddDatatables1', function(e){
    e.preventDefault();
    $( '#addFormContainer' ).toggleClass( 'hide' );
    $( '#formAddDatatables1' )[0].reset();
  })
  .on( 'submit', '#formAddDatatables1', function(e){
    e.preventDefault();

    var $this = $( this ),
    datas = $this.serializeArray(); // or use $this.serialize()

    // do server action to save change here ( ajax )
    // ...
    // just simple rule after ajax is done (demo)
    $.each( datas, function( i, data ){
      console.log( data.name + ' = ' + data.value );
    });

    // add new row to datatables using datatables plugin fnAddDataAndDisplay([ 1,2,3,... ]) ( see scripts/demo/datatables-plugins.js )
    // or you can just use fnAddData([ 1,2,3,... ]) - without any datatables plugin
    var addData = datatables1.fnAddDataAndDisplay([
      datas[0].value,
      datas[1].value,
      datas[2].value,
      datas[3].value,
      datas[4].value
      ]),
    newRow = addData.nTr,
      newID = datatables1.fnGetData().length; // just sample id (on real case: get it from server callback)

    // adding data-id to new row
    // then make it selected and enable to delete or edit
    datatables1.$( 'tr.active' ).removeClass( 'active' );
    $( newRow ).attr( 'data-id', 'datatables1_' + newID )
    .addClass( 'active' );
    // activate actions edit & delete
    $( '.datatables1-actions' ).removeClass( 'disabled' );
    // reset form
    $( '#formAddDatatables1' )[0].reset();
  })
  // edit rule
  .on( 'click', '#edit-datatables1, #hideEditDatatables1', function(e){
    e.preventDefault();
    $( '#editFormContainer' ).toggleClass( 'hide' );
    // get data selecter row
    getDataSelected();
  })
  .on( 'submit', '#formEditDatatables1', function(e){
    e.preventDefault();

    var $this = $( this ),
    datas = $this.serializeArray(); // or use $this.serialize()

    // do server action to save change here ( ajax )
    // ...
    // just simple rule after ajax is done to demo
    $.each( datas, function( i, data ){
      console.log( data.name + ' = ' + data.value );
    });

    // change data selected row datatables
    // get data from selected row
    var dataSelected = datatables1.$( 'tr.active' ),
    node = getSelectedNode( datatables1 ),
    dataUpdate = [ datas[1].value, datas[2].value, datas[3].value, datas[4].value, datas[5].value ];

    dataSelected.data( 'id', datas[0].value );
    datatables1.fnUpdate( dataUpdate, node );

    // keep display on changed row
    datatables1.fnDisplayRow( node );

    // hide form edit
    $( '#editFormContainer' ).addClass( 'hide' );
  });

  // simple fn to get a single node of selected row
  var getSelectedNode = function ( datatables ){
    var node,
    nodes = datatables.fnGetNodes();

    for ( var i=0 ; i < nodes.length ; i++ ){
      if ( $( nodes[i] ).hasClass( 'active' ) )
      {
        node =  nodes[i];
      }
    }

    return node;
  },

  // get data from selected row
  getDataSelected = function(){
    var dataSelected = datatables1.$( 'tr.active' ),
    datatables1ID = dataSelected.data( 'id' ),
    engineRender = dataSelected.children( 'td:eq(0)' ).text(),
    browser = dataSelected.children( 'td:eq(1)' ).text(),
    platform = dataSelected.children( 'td:eq(2)' ).text(),
    engineVersion = dataSelected.children( 'td:eq(3)' ).text(),
    cssGrade = dataSelected.children( 'td:eq(4)' ).text();

    // set data form edit
    $( '#datatables1ID' ).val( datatables1ID );
    $( '#editEngine' ).val( engineRender );
    $( '#editBrowser' ).val( browser );
    $( '#editPlatform' ).val( platform );
    $( '#editVersion' ).val( engineVersion );

    // set data on input select
    $( '#editGrade' ).val( cssGrade );
  };


  // Table Tools
  // tabletools setting
  /*
   * TableTools Bootstrap compatibility
   * Required TableTools 2.1+
   */
   if ( $.fn.DataTable.TableTools ) {
    // Set the classes that TableTools uses to something suitable for Bootstrap
    $.extend( true, $.fn.DataTable.TableTools.classes, {
      'container': 'DTTT btn-group',
      'buttons': {
        'normal': 'btn btn-default',
        'disabled': 'disabled'
      },
      'collection': {
        'container': 'DTTT_dropdown dropdown-menu',
        'buttons': {
          'normal': '',
          'disabled': 'disabled'
        }
      },
      'print': {
        'info': 'DTTT_print_info'
      },
      'select': {
        'row': 'selected'
      }
    } );

    // Have the collection use a bootstrap compatible dropdown
    $.extend( true, $.fn.DataTable.TableTools.DEFAULTS.oTags, {
      'collection': {
        'container': 'ul',
        'button': 'li',
        'liner': 'a'
      }
    } );
  }
  // datatables2
  $('#datatables2').dataTable({
    'autoWidth': false,
    'sDom': '<"TTT_btn-group-wrapper tt-actions-demo"T><"row"<"col-sm-12"<"pull-right"f><"pull-left"l>r<"clearfix">>>t<"row"<"col-sm-12"<"pull-left"i><"pull-right"p><"clearfix">>>',
    // 'sPaginationType': 'two_button',
    'sAjaxSource': '_includes/data-source.json',
    'oTableTools': {
      'aButtons': [
      {
        'sExtends': 'copy',
        'sButtonText': '<i class="fa fa-clone fa-lg" title="Copy"></i>',
        'sButtonClass': 'btn btn-default btn-icon'
      },
      {
        'sExtends': 'print',
        'sButtonText': '<i class="icon-printer fa-lg" title="Print"></i>',
        'sButtonClass': 'btn btn-default btn-icon'
      },
      {
        'sExtends': 'collection',
        'sButtonText': '<i class="fa fa-floppy-o fa-lg" title="Save as..."></i> <i class="fa fa-angle-down"></i>',
        'sButtonClass': 'btn btn-default btn-icon',
        'aButtons': [ 'xls', 'csv', 'pdf' ]
      }
      ],
      'sSwfPath': 'scripts/swf/copy_csv_xls_pdf.swf'
    },
    'fnInitComplete': function(settings) {
      var $wrapperTable = $(settings.nTable).closest('.dataTables_wrapper');

      // replace select
      $wrapperTable.find('.dataTables_length select').wrap('<label class="select select-inline select-sm"></label>');

      // place tableTools buttons to panel-actions
      $('.tt-actions-demo').prependTo('#tt-actions');

      var $nTable = $(settings.nTable);
      $nTable.closest( '.dataTables_wrapper' ).find( '.dataTable' ).wrap('<div class="table-responsive"></div>');
    }
  });



  // adding custom styles to all .datatables
  $('.dataTable').each(function(){
    var datatables = $( this );
    // SEARCH - Add the placeholder for Search and Turn this into in-line form control
    var searchInput = datatables.closest('.dataTables_wrapper').find('div[id$=_filter] input');
    searchInput.attr('placeholder', 'Search');
  });

})(window);