(function(){
  'use strict';

  var Bloodhound = window.Bloodhound;

  // TYPEAHEAD DEMO
  // Single dataset
  var substringMatcher = function(strs) {
    return function findMatches(q, cb) {
      var matches, substrRegex;

      // an array that will be populated with substring matches
      matches = [];

      // regex used to determine if a string contains the substring `q`
      substrRegex = new RegExp(q, 'i');

      // iterate through the pool of strings and for any string that
      // contains the substring `q`, add it to the `matches` array
      $.each(strs, function(i, str) {
        if (substrRegex.test(str)) {
          // the typeahead jQuery plugin expects suggestions to a
          // JavaScript object, refer to typeahead docs for more info
          matches.push({ value: str });
        }
      });

      cb(matches);
    };
  },
  teams =  [ 'Courtney Wilkins', 'Rama Obrien', 'Ross Mills', 'Craig Banks', 'Rae Franco', 'Darrel Carlson', 'Lynn Mcbride', 'Noelle Martinez', 'Risa Fletcher', 'Dennis Mejia', 'Blaze Eaton', 'Theodore Kelly', 'Roth Velazquez', 'Xena Holden', 'Deirdre Rodriquez', 'Nita Marquez', 'Amanda Hicks', 'Alan Ford', 'Judith Talley', 'Kuame Boyle'];

  $('#typeahead-local').typeahead({
    highlight: true,
    hint: true,
    minLength: 1
  },{
    name: 'teams',
    displayKey: 'value',
    source: substringMatcher(teams)
  });


  // Typeahead Prefetches
  var countries = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    limit: 10,
    prefetch: {
      url: '_includes/countries.json',
      filter: function(list) {
        return $.map(list, function(country) { return { name: country }; });
      }
    }
  });

  // kicks off the loading/processing of `local` and `prefetch`
  countries.initialize();

  // passing in `null` for the `options` arguments will result in the default
  // options being used
  $('#typeahead-prefetches').typeahead(null, {
    name: 'countries',
    displayKey: 'name',
    // `ttAdapter` wraps the suggestion engine in an adapter that
    // is compatible with the typeahead jQuery plugin
    source: countries.ttAdapter(),
    templates: {
      empty: function(){
        $( '#typeahead-nosuggest-helper' ).tooltip( 'show' );
        $( '#typeahead-prefetches-group' ).addClass( 'has-error' );
      },
      suggestion: function( datums ){
        if( datums ){
          $( '#typeahead-nosuggest-helper' ).tooltip( 'hide' );
          $( '#typeahead-prefetches-group' ).removeClass( 'has-error' );

          return '<p>'+ datums.name +'</p>';
        }
      }
    }
  }).on( 'typeahead:closed typeahead:cursorchanged typeahead:selected typeahead:autocompleted', function(){
    $( '#typeahead-nosuggest-helper' ).tooltip( 'hide' );
    $( '#typeahead-prefetches-group' ).removeClass( 'has-error' );
  });


  // Custom template
  var repos = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: '_includes/repos.json'
  });

  repos.initialize();

  var Handlebars = window.Handlebars;
  $('#typeahead-customtemplate').typeahead(null, {
    name: 'twitter-oss',
    displayKey: 'value',
    source: repos.ttAdapter(),
    templates: {
      empty: [
      '<div class="tt-message text-muted">',
      'unable to find any Projects that match the current query',
      '</div>'
      ].join('\n'),
      suggestion: Handlebars.compile( '<div><p class="pull-right text-muted"><i>{{language}}</i></p> <p><strong>{{name}}</strong></p> <p><small>{{description}}</small></p></div>')
    }
  });


  // Multiple Datasets
  var nbaTeams = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('team'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: '_includes/nba.json'
  });

  var nhlTeams = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('team'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: '_includes/nhl.json'
  });

  nbaTeams.initialize();
  nhlTeams.initialize();

  $('#multiple-datasets').typeahead({
    highlight: true
  },
  {
    name: 'nba-teams',
    displayKey: 'team',
    source: nbaTeams.ttAdapter(),
    templates: {
      header: '<div class="tt-heading"><h5 class="text-muted">NBA Teams</h5></div>'
    }
  },
  {
    name: 'nhl-teams',
    displayKey: 'team',
    source: nhlTeams.ttAdapter(),
    templates: {
      header: '<div class="tt-heading"><h5 class="text-muted">NHL Teams</h5></div>'
    }
  });
  // END TYPEAHEAD DEMO



  // TAGS INPUT
  $('[data-input="tags"], .input-tags').each(function(){
    var $this = $(this),
    placeholder = ($this.attr('placeholder') === undefined) ? '' : $this.attr('placeholder');

    $this.tagsInput({
      'width': '100%',
      'height': 'auto',
      'defaultText': placeholder,
      'placeholderColor' : 'rgba(22, 24, 27, 0.54)'
    });
  });
  $('.tagsinput input').on('focus', function(){
    var input = $(this),
    tagsInput = input.parent().parent();

    tagsInput.addClass('focus');
  })
  .on('blur', function(){
    var input = $(this),
    tagsInput = input.parent().parent();

    tagsInput.removeClass('focus');
  });
  // END TAGS INPUT


  // JQUERY MASK INPUT
  $('[data-mask="date"]').mask('00/00/0000');
  $('[data-mask="time"]').mask('00:00:00');
  $('[data-mask="date_time"]').mask('00/00/0000 00:00:00');
  $('[data-mask="zip"]').mask('00000-000');
  $('[data-mask="money"]').mask('000,000,000,000,000.00', {reverse: true});
  $('[data-mask="phone"]').mask('0000-0000');
  $('[data-mask="phone_with_ddd"]').mask('(00) 0000-0000');
  $('[data-mask="phone_us"]').mask('(000) 000-0000');
  $('[data-mask="cpf"]').mask('000.000.000-00', {reverse: true});
  $('[data-mask="ip_address"]').mask('099.099.099.099');
  $('[data-mask="percent"]').mask('##0,00%', {reverse: true});
  // END JQUERY MASK INPUT


  // SELECT2
  $('[data-input="select2"], .select2').each(function(){
    var $this = $(this),
    placeholder = ($this.attr('placeholder') === undefined) ? 'Select a choice' : $this.attr('placeholder');

    $this.select2({
      placeholder: placeholder
    });
  });
  $('[data-input="select2-tags"], .select2-tags').each(function(){
    var $this = $(this);

    $this.select2({
      tags: true,
      tokenSeparators: [',']
    });
  });
  // END SELECT2


  // SELECTBOXIT
  $('[data-input="selectboxit"], .selectboxit').each(function(){
    var $this = $(this);

    $this.selectBoxIt(this.dataset);
  });
  // END SELECTBOXIT


  // DATE RANGE PICKER DEMO
  var moment = window.moment;

  $('[data-input="daterangepicker"]').each(function(){
    var $this = $(this),
    dataset = $(this).data();
    dataset.applyClass = 'btn-primary';

    $this.daterangepicker(dataset);
  });

  $('#reportrange').on('click', function(e){
    e.preventDefault();
  })
  .daterangepicker({
    applyClass: 'btn-primary',
    ranges: {
      'Today': [moment(), moment()],
      'Yesterday': [moment().subtract('days', 1), moment().subtract('days', 1)],
      'Last 7 Days': [moment().subtract('days', 6), moment()],
      'Last 30 Days': [moment().subtract('days', 29), moment()],
      'This Month': [moment().startOf('month'), moment().endOf('month')],
      'Last Month': [moment().subtract('month', 1).startOf('month'), moment().subtract('month', 1).endOf('month')]
    },
    startDate: moment().subtract('days', 29),
    endDate: moment(),
    opens: 'left'
  },
  function(start, end) {
    $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
  })
  .find('span').html(moment().format('MMMM D, YYYY') + ' - ' + moment().format('MMMM D, YYYY'));

  // add animation on show/hide picker
  $('[data-input="daterangepicker"], #reportrange').on('show.daterangepicker', function(e, picker){
    var target = picker.container;
    target.velocity('transition.expandIn', 250);
  })
  .on('hide.daterangepicker', function(e, picker){
    var target = picker.container;
    target.css('display', 'block')
    .velocity('transition.slideUpOut', 250);
  });
  $('#reportrange').on('showCalendar.daterangepicker', function(e, picker){
    var target = picker.container.children('.calendar');
    target.velocity('transition.slideRightIn', 250);
  })
  .on('hide.daterangepicker', function(e, picker){
    var target = picker.container.children('.calendar');
    target.velocity('transition.slideRightOut', 250);
  });
  // END DATE RANGE PICKER DEMO



  // COLOR PICKER
  $('[data-input="colorpicker"]').each(function(){
    var $this = $(this);

    $this.minicolors({
      control: $this.data().control || 'hue',
      defaultValue: $this.data().defaultValue || '',
      inline: ($this.data().inline) ? 'true' : false,
      letterCase: $this.data().letterCase || 'lowercase',
      opacity: $this.data().opacity,
      position: $this.data().position || 'bottom left',
      theme: 'bootstrap'
    });
  });
  // END COLOR PICKER

})(window);