/*
 * Copyright (c) 2016
 * Licensed under the MIT license.
 */
(function($) {

    $.fn.extend({
        floatingLabels: function(options) {

            var defaults = {
                errorBlock: false,
                isRequired: false,
                isPatternValid: false,
                isEmailValid: false,
                isFieldEqualTo: false,
                minLength: 0,
				maxLength: 20
            };

            function isEmailValid(email) {
				if(!email) {
					return false;
				}
                var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
                return regex.test(email);
            }

            options = $.extend(defaults, options);
            $(this).parent('.form-group.floating-labels').addClass('is-empty');
            $(this).parent().find('.error-block, .success-block').addClass('hidden');

            $(this).focus(function() {
                $(this).parent('.form-group.floating-labels').addClass('has-focus');
            }).blur(function() {
                $(this).parent('.form-group.floating-labels').removeClass('has-focus');

                var value = $(this).val();

                //is-empty
                if (value) {
                    $(this).parent('.form-group.floating-labels').removeClass('is-empty');
                }
                if (!value) {
                    $(this).parent('.form-group.floating-labels').addClass('is-empty');
                }

                //error-block
                if (options.errorBlock && value) {
                    $(this).parent('.form-group.floating-labels').removeClass('has-error');
                    $(this).parent('.form-group.floating-labels').find('.error-block').addClass('hidden').text('');
                }
                if (options.errorBlock && !value) {
                    $(this).parent('.form-group.floating-labels').addClass('has-error');
                    $(this).parent('.form-group.floating-labels').find('.error-block').removeClass('hidden').text(options.errorBlock);
					return false;
                }

				if(options.isEmailValid) {
					if(isEmailValid(value)) {
						$(this).parent('.form-group.floating-labels').removeClass('has-error');
						$(this).parent('.form-group.floating-labels').find('.error-block').addClass('hidden').text();
					} 
					if(!isEmailValid(value)) {
						$(this).parent('.form-group.floating-labels').addClass('has-error');
						$(this).parent('.form-group.floating-labels').find('.error-block').removeClass('hidden').text(options.isEmailValid);
						return false;
					} 
				} 

				if(options.minLength && value.length < options.minLength) {
					$(this).parent('.form-group.floating-labels').addClass('has-error');
					$(this).parent('.form-group.floating-labels').find('.error-block').removeClass('hidden').text(options.errorBlock);
					return false;
				}

				if(options.isFieldEqualTo) {
					var compareTo = options.isFieldEqualTo.val();
					if (value === compareTo) {
						$(this).parent('.form-group.floating-labels').removeClass('has-error');
						$(this).parent('.form-group.floating-labels').find('.error-block').addClass('hidden').text('');
					}
					if (value !== compareTo) {
						$(this).parent('.form-group.floating-labels').addClass('has-error');
						$(this).parent('.form-group.floating-labels').find('.error-block').removeClass('hidden').text(options.errorBlock);
						return false;
					}
				}

            });

        }
    });

}(jQuery));
