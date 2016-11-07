/**
 * @author Batch Themes Ltd.
 */
(function() {
    'use strict';

    $(function() {
        $('.horizontal-navigation-3 [data-click]').on('click', function(e) {
            var action = $(this).data('click');
            var id = $(this).data('id');

            if (action === 'set-layout') {
                e.preventDefault();
                setLayout(id);
                return false;
            }

        });
    });

})();
