/**
 * @author Batch Themes Ltd.
 */
(function() {
    'use strict';

    $(function() {
        $('.navbar-1 [data-click]').on('click', function(e) {
            var action = $(this).data('click');
            var id = $(this).data('id');

            if (action === 'toggle-search') {
                e.preventDefault();
                toggleSearch();
                return false;
            }
            if (action === 'toggle-fullscreen-mode') {
                e.preventDefault();
                toggleFullscreenMode();
                return false;
            }
            if (action === 'toggle-layout') {
                e.preventDefault();
                toggleLayout();
                return false;
            }
            if (action === 'toggle-right-sidebar') {
                e.preventDefault();
                toggleRightSidebar();
                return false;
            }
            if (action === 'toggle-theme-selector') {
                e.preventDefault();
                toggleThemeSelector();
                return false;
            }
            if (action === 'set-layout') {
                e.preventDefault();
                setLayout(id);
                return false;
            }
            if (action === 'toggle-direction') {
                e.preventDefault();

                var direction = $('body').attr('data-direction');
                direction = direction == 'rtl' ? 'ltr' : 'rtl';
                $('body').attr('data-direction', direction);

                var config = $.localStorage.get('config');
                config.direction = direction;
                $.localStorage.set('config', config);

                var directionText = 'RTL';
                if (direction === 'rtl') {
                    directionText = 'LTR';
                }
                $('.direction').text(directionText);

                return false;
            }
        });

        var direction = $('body').attr('data-direction');
        var directionText = 'RTL';
        if (direction === 'rtl') {
            directionText = 'LTR';
        }
        $('.direction').text(directionText);

        $('.theme-selector [data-click]').on('click', function(e) {
            var action = $(this).data('click');
            var id = $(this).data('id');

            if (action === 'set-palette') {
                e.preventDefault();
                setPalette(id);
                return false;
            }

        });

    });

})();
