/*
 * Yabroad text-minify jquery plugin
 *
 */
;(function($) {
    $.fn.textminify = function(options) {
        opts = $.extend({}, $.fn.textminify.defaults, options);

        /* ------------------------------------- */
        /* Init text-minify */
        /* ------------------------------------- */
        return this.each(function() {
            var container = this;
            var $content = $(container).children(".ya-text-minify-content");
            var $summary = $(container).children(".ya-text-minify-short");
            if ($content.text() == $summary.text()) {
                $(container).children(".ya-text-minify-btn").hide();
                $(container).data("active", "active");
            }
            if ($(container).data("active")) {
                return;
            }
            $(container).children(".ya-text-minify-btn").click(function() {
                var $btn = $(this);
                var $content = $(container).children(".ya-text-minify-content");
                var $summary = $(container).children(".ya-text-minify-short");
                var minified = ($content.css("display") == 'none');

                if (minified) {
                    $btn.hide();
                    $btn.children('i').removeClass('icon-chevron-down');
                    $btn.children('i').addClass('icon-chevron-up');
                    $summary.hide();
                    $content.show();
                    $btn.show('fast', 'linear');
                } else {
                    $btn.hide();
                    $btn.children('i').removeClass('icon-chevron-up');
                    $btn.children('i').addClass('icon-chevron-down');
                    $summary.show();
                    $content.hide();
                    $btn.show('fast', 'linear');
                }
            });
            $(container).data("active", "active");
        });
    };

    /* ------------------------------------- */
    /* Default options */
    /* ------------------------------------- */
    $.fn.textminify.defaults = {
    };

})(jQuery);

jQuery(document).ready(function() {
    jQuery(".text-minify-container").textminify();
});
