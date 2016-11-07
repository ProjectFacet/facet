/**
 * @author Batch Themes Ltd.
 */
(function() {
    'use strict';

    $(function() {
        $('.sidebar-1 [data-click]').on('click', function(e) {
            var action = $(this).data('click');
            var id = $(this).data('id');

            if (action === 'toggle-profile') {
                e.preventDefault();
                toggleProfile();
                return false;
            }
            if (action === 'toggle-section') {
                e.preventDefault();
                toggleSection(id);
                return false;
            }
            if (action === 'set-layout') {
                e.preventDefault();
                setLayout(id);
                return false;
            }
            if (action === 'toggle-layout') {
                e.preventDefault();
                toggleLayout();
                return false;
            }
            if (action === 'toggle-sidebar') {
                e.preventDefault();
                toggleSidebar();
                return false;
            }

        });

		var id = false;
        var url = window.location.href;

		$('.l2 a').each(function(v, k) {
			var item = $(this);
			var href = item.attr('href');
			if(href && url.indexOf(href) > -1) {
				item.addClass('sideline-active');
			}
		});

		if(url.match(/ui-elements-/gi)) {
			id = 'ui';
			toggleSection(id);
			return false;
		} else if(url.match(/dashboards-/)) {
			id = 'dashboards';
			toggleSection(id);
			return false;
		} else if(url.match(/widgets-/)) {
			id = 'widgets';
			toggleSection(id);
			return false;
		} else if(url.match(/utilities-/)) {
			id = 'utilities';
			toggleSection(id);
			return false;
		} else if(url.match(/icons-/)) {
			id = 'icons';
			toggleSection(id);
			return false;
		} else if(url.match(/forms-/)) {
			id = 'forms';
			toggleSection(id);
			return false;
		} else if(url.match(/tables-/)) {
			id = 'tables';
			toggleSection(id);
			return false;
		} else if(url.match(/e-commerce-/)) {
			id = 'e-commerce';
			toggleSection(id);
			return false;
		} else if(url.match(/email-/)) {
			id = 'email';
			toggleSection(id);
			return false;
		} else if(url.match(/charts-/)) {
			id = 'charts';
			toggleSection(id);
			return false;
		} else if(url.match(/pages-/)) {
			id = 'pages';
			toggleSection(id);
			return false;
		} else if(url.match(/extras-/)) {
			id = 'extras';
			toggleSection(id);
			return false;
		}

    });

})();
