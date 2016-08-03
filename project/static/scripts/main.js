/**
 * @author Batch Themes Ltd.
 */
(function() {
    'use strict';

    $(function() {

        var config = {
            name: 'Marino',
            theme: 'palette-2',
            palette: getPalette('palette-2'),
            layout: 'horizontal-navigation-3',
            direction: 'ltr', //ltr or rtl
            colors: getColors()
        };

        //$.removeAllStorages();
        if ($.localStorage.isEmpty('config') || !($.localStorage.get('config'))) {
            $.removeAllStorages();
            $.localStorage.set('config', config);
        }
        //var config = $.localStorage.get('config');

        var el = $('.main');
        var wh = $(window).height();
        el.css('min-height', wh + 'px');

        var el2 = $('.main-view');
        el2.css('min-height', (wh - 54) + 'px');


    });
})();
