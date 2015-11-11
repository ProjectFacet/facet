(function() {
  'use strict';

  // Basic Validation
  $('#basic-validate').validate({
    rules: {
      basicText: {
        required: true,
        minlength: 2
      },
      basicPasswd: {
        required: true,
        minlength: 5
      },
      confirmBasicPasswd: {
        required: true,
        minlength: 5,
        equalTo: '#basicPasswd'
      },
      basicEmail: {
        required: true,
        email: true
      },
      basicSelect: {
        required: true
      },
      basicFile: {
        required: true
      },
      basicAgree: 'required'
    },
    errorElement: 'div',
    errorClass: 'text-danger',
    errorPlacement: function(error, element) {
      var $formGroup = element.closest('.form-group');
      error.appendTo($formGroup);
    },
    highlight: function(element) {
      var $formGroup = $(element).closest('.form-group');
      $formGroup.addClass('has-error');
    },
    unhighlight: function(element) {
      var $formGroup = $(element).closest('.form-group');
      $formGroup.removeClass('has-error');
    },
    showErrors: function() {
      var $form = $(this.currentForm),
        $panel = $form.closest('.panel'),
        errors = this.numberOfInvalids();

      this.defaultShowErrors();

      if (errors) {
        // change panel state
        $panel.removeClass('panel-default');
        $panel.addClass('panel-danger');

        // disable submit button
        $form.find('[type="submit"]').attr('disabled', true);

        // remove existing error summary
        $panel.find('.panel-title > small').remove();
        // Display a summary of invalid fields as a subtitle
        $panel.find('.panel-title').append(' <small>' + errors + ' field(s) are invalid</small>');
      } else {
        // change panel state
        $panel.removeClass('panel-danger');
        $panel.addClass('panel-default');

        // enable submit button
        $form.find('[type="submit"]').attr('disabled', false);

        // remove error summary
        $panel.find('.panel-title > small').remove();
      }
    }
  });


  // Validation using tooltip
  $('#tip-validate').validate({
    rules: {
      tipText: {
        required: true,
        minlength: 2
      },
      tipPasswd: {
        required: true,
        minlength: 5
      },
      confirmTipPasswd: {
        required: true,
        minlength: 5,
        equalTo: '#tipPasswd'
      },
      tipEmail: {
        required: true,
        email: true
      },
      tipSelect: {
        required: true
      },
      tipFile: {
        required: true
      },
      tipAgree: 'required'
    },
    showErrors: function(errorMap, errorList) {
      var $form = $(this.currentForm),
        errors = this.numberOfInvalids();

      if (errors) {
        // disable submit button
        $form.find('[type="submit"]').attr('disabled', true);
      } else {
        // enable submit button
        $form.find('[type="submit"]').attr('disabled', false);
      }

      // Clean up any tooltips for valid elements
      $.each(this.validElements(), function(i, elem) {
        var $elem = $(elem),
          $targetTip = ($elem.is('[type="checkbox"]')) ? $elem.next().children('.fake-addon') : $elem.next(),
          $formGroup = $elem.closest('.form-group');

        // remove error state
        $formGroup.removeClass('has-error');
        // remove tooltip
        $targetTip.tooltip('destroy');
      });

      // Create new tooltips for invalid elements
      $.each(errorList, function(i, error) {
        var $elem = $(error.element),
          $targetTip = ($elem.is('[type="checkbox"]')) ? $elem.next().children('.fake-addon') : $elem.next(), // targeting the tooltip on addon input
          $formGroup = $elem.closest('.form-group'),
          data = {};

        // adding error state
        $formGroup.addClass('has-error');

        // tooltip options
        data.template = '<div class="tooltip tooltip-danger"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>';
        data.placement = ($elem.is('[type="checkbox"]')) ? 'bottom' : 'left';
        data.container = 'body';
        data.title = error.message;
        data.trigger = 'focus'; // use focus, so tooltip still available until element is valid

        // destroy existing tooltip
        $targetTip.tooltip('destroy');

        // create a new tooltip
        $targetTip.tooltip(data)
          .tooltip('show');
      });
    }
  });



  // Validate state w/ icon
  $('#stateNumber').mask('#999999999.00');
  $('#stateDigits').mask('0000000000');

  $('#state-validate').validate({
    rules: {
      stateText: {
        required: true,
        minlength: 2
      },
      stateEmail: {
        required: true,
        email: true
      },
      stateUrl: {
        required: true,
        url: true
      },
      stateNumber: {
        required: true,
        number: true
      },
      stateDigits: {
        required: true,
        digits: true
      },
      stateCard: {
        required: true,
        creditcard: true
      }
    },
    errorElement: 'div',
    errorClass: 'text-danger',
    errorPlacement: function(error, element) {
      var $formGroup = element.closest('.form-group');
      error.appendTo($formGroup);
    },
    highlight: function(element) {
      var $formGroup = $(element).closest('.form-group'),
        $icon = $formGroup.children('.form-control-feedback');

      $formGroup.removeClass('has-success')
        .addClass('has-error');
      $icon.attr('class', 'icon-close form-control-feedback');
    },
    unhighlight: function(element) {
      var $formGroup = $(element).closest('.form-group'),
        $icon = $formGroup.children('.form-control-feedback');

      $formGroup.removeClass('has-error')
        .addClass('has-success');

      $icon.attr('class', 'icon-check form-control-feedback');
    },
    showErrors: function() {
      var $form = $(this.currentForm),
        errors = this.numberOfInvalids();

      this.defaultShowErrors();

      if (errors) {
        // disable submit button
        $form.find('[type="submit"]').attr('disabled', true);

        $('#indicator-fills > .progress-bar').removeClass('progress-bar-success');
      } else {
        // enable submit button
        $form.find('[type="submit"]').attr('disabled', false);

        $('#indicator-fills > .progress-bar').addClass('progress-bar-success');
      }

      var inputs = Object.keys(this.settings.rules).length,
        step = inputs - errors;
      $('#indicator-fills > .progress-bar').animate({
        width: (step / inputs * 100) + '%'
      });

      if (step) {
        $('#indicator-fills > .progress-bar').html('<span class="progress-text">' + step + '/' + inputs + '</span>');
      } else {
        $('#indicator-fills > .progress-bar').html('');
      }
    }
  });



  // validation Advance elements
  var advanceValidate = $('#adv-validate').validate({
    ignore: '.ignore',
    rules: {
      typeahead: {
        required: true
      },
      tagsinput: {
        required: true
      },
      s2Dropdown: {
        required: true
      },
      s2Tags: {
        required: true
      },
      selectboxit: {
        required: true
      }
    },
    messages: {
      s2Dropdown: {
        required: 'This field is required!'
      },
      s2Tags: {
        required: 'This field is required!'
      }
    },
    errorElement: 'div',
    errorClass: 'text-danger',
    errorPlacement: function(error, element) {
      var $formGroup = element.closest('.form-group');
      error.appendTo($formGroup);
    },
    highlight: function(element) {
      var $formGroup = $(element).closest('.form-group');

      $formGroup.removeClass('has-success')
        .addClass('has-error');
    },
    unhighlight: function(element) {
      var $formGroup = $(element).closest('.form-group');

      $formGroup.removeClass('has-error')
        .addClass('has-success');
    },
    showErrors: function() {
      var $form = $(this.currentForm),
        errors = this.numberOfInvalids();

      this.defaultShowErrors();

      if (errors) {
        // disable submit button
        $form.find('[type="submit"]').attr('disabled', true);
      } else {
        // enable submit button
        $form.find('[type="submit"]').attr('disabled', false);
      }
    }
  });

  // initial elements
  // select2
  $('#s2Dropdown, #s2Tags').select2({
    placeholder: 'Select...'
  });
  $('#s2Dropdown, #s2Tags').on('change', function() {
    advanceValidate.element($(this));
  });
  // end select2

  // Typeahead Single dataset
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
            matches.push({
              value: str
            });
          }
        });

        cb(matches);
      };
    },
    teams = ['Courtney Wilkins', 'Rama Obrien', 'Ross Mills', 'Craig Banks', 'Rae Franco', 'Darrel Carlson', 'Lynn Mcbride', 'Noelle Martinez', 'Risa Fletcher', 'Dennis Mejia', 'Blaze Eaton', 'Theodore Kelly', 'Roth Velazquez', 'Xena Holden', 'Deirdre Rodriquez', 'Nita Marquez', 'Amanda Hicks', 'Alan Ford', 'Judith Talley', 'Kuame Boyle'];

  $('#typeahead').typeahead({
    highlight: true,
    hint: true,
    minLength: 1
  }, {
    name: 'teams',
    displayKey: 'value',
    source: substringMatcher(teams)
  });
  // end typeahead

  // Tagsinputs
  $('#tagsinput').tagsInput({
    'width': '100%',
    'height': 'auto',
    'placeholderColor': 'rgba(79, 86, 97, 0.87)',
    'onAddTag': function() {
      advanceValidate.element($(this));
    },
    'onRemoveTag': function() {
      advanceValidate.element($(this));
    }
  });
  $('.tagsinput input').on('focus', function() {
      var input = $(this),
        tagsInput = input.parent().parent();

      tagsInput.addClass('focus');
    })
    .on('blur', function() {
      var input = $(this),
        tagsInput = input.parent().parent();

      tagsInput.removeClass('focus');
    });
  // end tagsinput

  // SELECTBOXIT
  $('#selectboxit').selectBoxIt({
    defaultText: 'Select city',
    change: function() {
      advanceValidate.element($(this));
    }
  });
  // END SELECTBOXIT

})(window);
