/**
 * @author Batch Themes Ltd.
 */
function detectIE() {
    /**
     * detect IE
     * returns version of IE or false, if browser is not Internet Explorer
     */
    var ua = window.navigator.userAgent;

    var msie = ua.indexOf('MSIE ');
    if (msie > 0) {
        // IE 10 or older => return version number
        return parseInt(ua.substring(msie + 5, ua.indexOf('.', msie)), 10);
    }

    var trident = ua.indexOf('Trident/');
    if (trident > 0) {
        // IE 11 => return version number
        var rv = ua.indexOf('rv:');
        return parseInt(ua.substring(rv + 3, ua.indexOf('.', rv)), 10);
    }

    var edge = ua.indexOf('Edge/');
    if (edge > 0) {
        // Edge (IE 12+) => return version number
        return parseInt(ua.substring(edge + 5, ua.indexOf('.', edge)), 10);
    }

    // other browser
    return false;
};

function toggleSearch() {
    var navbarDrawer = $('.navbar-drawer');
    navbarDrawer.toggleClass('active');
};

function toggleSearchInput() {
    $('.navbar-search').toggleClass('navbar-search-hidden');
};

function toggleRightSidebar() {
    $('.right-sidebar-outer').toggleClass('show-from-right');
};

function toggleLayout() {

    var config = $.localStorage.get('config');
    var layout = config.layout;

    if (layout === 'default-sidebar') {
        $('body').attr('data-layout', 'collapsed-sidebar');
        config.layout = 'collapsed-sidebar';
        $.localStorage.set('config', config);
    } else if (layout === 'collapsed-sidebar') {
        $('body').attr('data-layout', 'default-sidebar');
        config.layout = 'default-sidebar';
        $.localStorage.set('config', config);
    } else {
        $('body').toggleClass('layout-collapsed');
    }
};

function toggleFullscreenMode() {
    $(document).fullScreen(true);
};

function toggleThemeSelector() {
    $('.theme-selector').toggleClass('show-theme-selector');
};

function setPalette(palette) {
    var config = $.localStorage.get('config');
    config.theme = palette;
    config.palette = getPalette(palette);
    $.localStorage.set('config', config);
    $('body').attr('data-palette', palette);
    window.location.reload();
};

function toggleSection(id) {
    $('.section-' + id).toggleClass('active');
    $('.fa-caret-down.icon-' + id).toggleClass('fa-rotate-180');
};

function toggleProfile() {
    $('.account-links').toggleClass('account-links-open');
    $('.fa-caret-down.icon-toggle-profile').toggleClass('fa-rotate-180');
};

function toggleSidebar() {
    $('body').toggleClass('layout-collapsed');
};

function setLayout(layout) {

    var config = $.localStorage.get('config');
    config.layout = layout;

    console.log('new config', config);
    $.removeAllStorages();
    $.localStorage.set('config', config);

    $('body').removeClass('layout-collapsed');
    $('body').attr('data-layout', layout);
};

//http://www.sitepoint.com/javascript-generate-lighter-darker-color/
function colorLuminance(hex, lum) {

    // validate hex string
    hex = String(hex).replace(/[^0-9a-f]/gi, '');
    if (hex.length < 6) {
        hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
    }
    lum = lum || 0;

    // convert to decimal and change luminosity
    var rgb = "#",
        c, i;
    for (i = 0; i < 3; i++) {
        c = parseInt(hex.substr(i * 2, 2), 16);
        c = Math.round(Math.min(Math.max(0, c + (c * lum)), 255)).toString(16);
        rgb += ("00" + c).substr(c.length);
    }

    return rgb;
};

function lighten(col, amt) {
    amt = Math.abs(amt);
    amt = amt / 100;
    return colorLuminance(col, amt);
};

function darken(col, amt) {
    amt = Math.abs(amt);
    amt = (amt / 100) * -1;
    return colorLuminance(col, amt);
};

function random(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
};
