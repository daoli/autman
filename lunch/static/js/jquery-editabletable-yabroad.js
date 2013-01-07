/*
 * Yabroad editable table jquery plugin
 *
 * Depends on jquery-ismouseover
 */
;(function($) {
    $.fn.editabletable = function(options) {
        opts = $.extend({}, $.fn.editabletable.defaults, options);

        /* ------------------------------------- */
        /* Internal functions */
        /* ------------------------------------- */
        function generate_display_field(field) {
            var res = '<span class="ya-editable-display-field" data-target="' + $(field).attr("name") + '">';
            var link = get_display_link(field);
            if (link) {
                res += '<a href="' + link + '">';
            }
            res += $(field).val();
            if (link) {
                res += '</a>';
            }
            res += '</span>';
            return res;
        }

        function set_editable(row) {
            $(row).find('.ya-editable-display-field').hide();
            if (!$(row).data("editable")) {
                $(row).data("editable", "editable");
                $(row).find('.ya-editable-field').each(function() {
                    $(this).show();
                })
            }
        }

        function row_value_changed(row) {
            changed = false;
            $(row).find('.ya-editable-field').each(function() {
                var display = $(row).find('span[data-target="' + $(this).attr("name") + '"]');
                if ($(display).text() != $(this).val()) {
                    changed = true;
                }
            });
            return changed;
        }

        function get_display_link(field) {
            return $(field).data('display-link');
        }

        function update_display_field(row) {
            $(row).find('.ya-editable-field').each(function() {
                var display = $(row).find('span[data-target="' + $(this).attr("name") + '"]');
                if (get_display_link(this)) {
                    $(display).children('a').text($(this).val());
                } else {
                    $(display).text($(this).val());
                }
            });
        }

        function revert_editable_field(row) {
            $(row).find('.ya-editable-field').each(function() {
                var display = $(row).find('span[data-target="' + $(this).attr("name") + '"]');
                $(this).val($(display).text());
            });
        }

        // Provide rich APIs for external access on each row.
        function wrap_row_object(row) {
            row.value_changed = function () {
                return row_value_changed(this);
            };
            row.sync_display = function () {
                return update_display_field(this);
            };
            row.revert_change = function () {
                return revert_editable_field(this);
            };
        }

        function close_editable(row) {
            wrap_row_object(row);
            opts.row_update_callback(row);
            $(row).data("editable", '');
            $(row).find('.ya-editable-field').each(function() {
                $(this).hide();
                $(row).find('.ya-editable-display-field').show();
            });
        }

        function init_table(table, options) {
            $(table).find(".ya-editable-row").each(function() {
                $(this).dblclick(function() {
                    set_editable(this);
                });
                $(this).find('.ya-editable-field').each(function() {
                    $(generate_display_field(this)).insertAfter($(this));
                });
            });
        }

        /* ------------------------------------- */
        /* Init editable table */
        /* ------------------------------------- */
        $("html").click(function() {
            if (!$('.ya-editable-table').ismouseover()) {
                $(".ya-editable-row").each(function() {
                    close_editable(this);
                });
            }
        });
        return this.each(function() {
            init_table(this, opts);
        });
    };

    /* ------------------------------------- */
    /* Default options */
    /* ------------------------------------- */
    $.fn.editabletable.defaults = {
        'row_update_callback': default_row_update_callback,
    };

    function default_row_update_callback(row) {
        //do nothing
    }
})(jQuery);
