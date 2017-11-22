(function() {
    'use strict';
    $(function() {
        var config = $.localStorage.get('config');
        $('body').attr('data-layout', config.layout);
        $('body').attr('data-palette', config.theme);
        $('body').attr('data-direction', config.direction);
        $('.tree').treegrid();
        var count_root_elements = 20;
        var count_deep = 5;
        for (var i = 0; i < count_root_elements; i++) {
            var tr = $("<tr></tr>").addClass("treegrid-" + i + "-0").appendTo($('.large-tree')).html("<td>Root node " + i + "</td><td>Additional info</td>");
            for (var j = 1; j < count_deep; j++) {
                $("<tr></tr>").addClass("treegrid-" + i + "-" + j).addClass("treegrid-parent-" + i + "-" + (j - 1)).appendTo($('.large-tree')).html("<td>Child node " + i + "-" + j + "</td><td>Additional info</td>");
            }
        }
        $('.large-tree').treegrid();
    });
})();
