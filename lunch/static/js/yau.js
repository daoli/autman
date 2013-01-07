// Require: underscore, backbone, jquery, ya_global.

window.ya['PagingMeta'] = Backbone.Model.extend({
        limit: 0,
        next: '',
        offset: 0,
        previous: '',
        totoal_count: 0
});

var yau = {
    static_url: ya['_env']['static_url'],

    /* Render the given underscore template and data with extra data from ya_global env */
    render_template: function(tmpl, data) {
        var ya = window.ya;
        compiled = _.template(tmpl);

        data.ENV = ya._env;
        return compiled(data);
    },

    /* instantiate a give backbone model. */
    instantiate: function(class_name) {
        var ya = window.ya;
        if (!_.has(ya, class_name)) {
            return null;
        }
        var cls = ya[class_name];
        return new cls();
    },

    /* Get init data from ya_global environment by a given path. */
    load_initdata: function(attr_path) {
        var ya = window.ya;
        if (!_.has(ya, '_init_data')) {
            return null;
        }
        init_data = ya._init_data;
        res = init_data;
        parts = attr_path.split('.');
        for (var i in parts) {
            if (_.has(res, parts[i])) {
                res = res[parts[i]];
            } else {
                return null;
            }
        }
        return res;
    },

    /* datapicker wrapper */
    datepicker: function($trigger, $dataholder) {
        $trigger.DatePicker({
            format:'Y-m-d',
            date: $dataholder.val(),
            current: $dataholder.val(),
            starts: 1,
            position: 'bottom',
            onBeforeShow: function(){
                var d = $dataholder.val();
                if (!d) {
                    d = new Date();
                    d = "" + d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate();
                }
                $trigger.DatePickerSetDate(d, true);
            },
            onChange: function(formated, dates){
                $dataholder.val(formated);
                $dataholder.trigger('focusout');
                $dataholder.focus();
            }
        });

        $dataholder.focusout(function() {
            var dateString = $dataholder.val();
            if (!dateString) {
                return;
            }
            var reggie = /(\d{4})-(\d{1,2})-(\d{1,2})/;
            var dateArray = reggie.exec(dateString);
            if (!dateArray) {
                $dataholder.val('');
                return;
            }

            var d = new Date((+dateArray[1]),(+dateArray[2])-1, (+dateArray[3]));
            $dataholder.val("" + d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate());
        });
    },

    sync_ui_to_backbone_model: function($ui, model) {

    }
};

/**
 * JQuery function to get query string.
 */
(function($){
    $.querystring = (function (a) {
        var i,
            p,
            b = {};
        if (a === "") { return {}; }
        for (i = 0; i < a.length; i += 1) {
            p = a[i].split('=');
            if (p.length === 2) {
                b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
            }
        }
        return b;
    }(window.location.search.substr(1).split('&')));
}(jQuery));


// adds .naturalWidth() and .naturalHeight() methods to jQuery
// for retreaving a normalized naturalWidth and naturalHeight.
(function($){
  var props = ['Width', 'Height'];
  var prop;

  while (prop = props.pop()) {
    (function (natural, prop) {
      $.fn[natural] = (natural in new Image()) ?
      function () {
        return this[0][natural];
      } :
      function () {
        var
        node = this[0],
        img,
        value;

        if (node.tagName.toLowerCase() === 'img') {
          img = new Image();
          img.src = node.src,
          value = img[prop];
        }
        return value;
      };
    }('natural' + prop, prop.toLowerCase()));
  }
}(jQuery));


/**
 * Plugin to notify user that ajax content is loading.
 */
;(function($) {
    $.fn.attach_ajax_loader = function(options) {
        var opts = $.extend({}, $.fn.attach_ajax_loader.defaults, options);

        /* ------------------------------------- */
        /* Init attach_ajax_loader */
        /* ------------------------------------- */
        return this.each(function() {
            var $self = $(this);
            var disable_evt_source = opts.disable_evt_source;

            function is_loaded() {
                return $self.data("ajax-loader-loaded") == "loaded";
            }

            function set_loaded() {
                $self.data("ajax-loader-loaded", "loaded");
            }

            function show_ajax_loader() {
                $self.attr('disabled', 'disabled');
                $loader.show();
            }

            function hide_ajax_loader() {
                $loader.hide();
                $self.removeAttr('disabled');
            }

            if (is_loaded()) {
                return;
            }

            img_src = yau.static_url + 'images/ajax-loader.gif';
            $loader = $('<img id="loader" style="display: none; margin-left: 6px" src="'+ img_src + '" alt="ajax-loading">');
            $loader.insertAfter($self);
            set_loaded();

            $self.bind('show_ajax_loader', show_ajax_loader);
            $self.bind('hide_ajax_loader', hide_ajax_loader);
        });
    };

    /* ------------------------------------- */
    /* Default options */
    /* ------------------------------------- */
    $.fn.attach_ajax_loader.defaults = {
        'disable_evt_source': true
    };

})(jQuery);

/**
 * Plugin for captcha.
 */
;(function($) {
    $.fn.build_captcha = function(options) {
        var opts = $.extend({}, $.fn.build_captcha.defaults, options);
        /* ------------------------------------- */
        /* Init build_captcha */
        /* ------------------------------------- */
        return this.each(function() {
            var $self = $(this);

            if (!$self.data("initialized")) {
                var $new_hash = $('<input name="' + opts.hash_field +
                                    '" type="hidden" id="id_' + opts.hash_field + '"/>');

                $new_hash.insertAfter($self);
                $self.attr('name', opts.ans_field);
                $self.data("initialized", true);
            }

            var $hash_field = $("#id_" + opts.hash_field);

            function reload_captcha() {
                $.ajax({
                    type: "POST",
                    url: '/api/v1/captcha/?format=json',
                    contentType: 'application/json; charset=utf-8',
                    data: '{}'
                })
                .done(function(data) {
                    $hash_field.val(data.key);
                    var img_field_id = "_widget_captch_id_" + opts.ans_field;
                    $("#"+img_field_id).remove();

                    var $img_field = $('<img id="' + img_field_id +
                                          '" class="' + opts.img_field_class +
                                          '" title="' + "Click for another captcha" +
                                          '" src="' + data.resource_uri + '"/>');
                    $img_field.insertAfter($self);
                    $img_field.click(function() {
                        reload_captcha();
                    });
                    $self.val('');
                })
                .fail(function(data) {
                    alert('failed to load captcha');
                });
            }
            reload_captcha();


        });
    };

    /* ------------------------------------- */
    /* Default options */
    /* ------------------------------------- */
    $.fn.build_captcha.defaults = {
        ans_field: 'captcha_1',
        hash_field: 'captcha_0',
        img_field_class: 'widget_captcha_image'
    };

    $(document).ready(function() {
        $(".widget_captche_holder").build_captcha();
    });
})(jQuery);

/**
 * Plugin for data selector.
 */
;(function($) {
    $.fn.data_selector = function(options) {
        var opts = $.extend({}, $.fn.data_selector.defaults, options);

        /* ------------------------------------- */
        /* Init data_selector */
        /* ------------------------------------- */
        return this.each(function() {
            var $self = $(this);
            if ($self.data("initialized")) {
                return;
            }
            yau.datepicker($self, $self);

            $self.data("initialized", true);
        });
    };

    /* ------------------------------------- */
    /* Default options */
    /* ------------------------------------- */
    $.fn.data_selector.defaults = {
    };

    $(document).ready(function() {
        $(".widget_date_holder").data_selector();
    });
})(jQuery);

/**
 * Plugin for choosing city.
 */
;(function($) {
    $.fn.city_selector = function(options) {
        var opts = $.extend({}, $.fn.city_selector.defaults, options);

        /* ------------------------------------- */
        /* Init city_selector */
        /* ------------------------------------- */
        return this.each(function() {
            var $self = $(this);
            if ($self.data("initialized")) {
                return;
            }
            var city_obj_id = $self.attr('id');
            var country_obj_id = '_widget_city_country_' + $self.attr('id');
            var region_obj_id = '_widget_city_region_' + $self.attr('id');
            var $country_obj = $('#' + country_obj_id);
            var $region_obj = $('#' + region_obj_id);
            var $city_obj = $self;

            function get_sub_content($obj) {
                var url;
                var $content_holder;
                if ($obj === null) {
                    url = '/api/v1/country/?limit=0';
                    $content_holder = $country_obj;
                    $country_obj.empty().append("<option selected='selected' value=''>----------</option>");
                    $region_obj.empty().append("<option selected='selected' value=''>Select a country first</option>");
                    $city_obj.empty().append("<option selected='selected' value=''>Select a region first</option>");
                } else if ($obj.attr('id') == country_obj_id) {
                    url = '/api/v1/region/?limit=0&country__id=' + $obj.val();
                    $content_holder = $region_obj;
                    $region_obj.empty().append("<option selected='selected' value=''>----------</option>");
                } else if ($obj.attr('id') == region_obj_id) {
                    url = '/api/v1/city/?limit=0&region__id=' + $obj.val();
                    $content_holder = $city_obj;
                    $city_obj.empty().append("<option selected='selected' value=''>----------</option>");
                }

//                $content_holder.append("<option selected='selected' value=''>Please select a country</option>");
                $.getJSON(url, function(data){
                    for (var i in data.objects) {
                        var obj = data.objects[i];
                        var name = obj.name;
                        var id = obj.id;
                        var child = "<option value='" + id + "'>" + name + "</option>";
                        $content_holder.append(child);
                    }
                });
            }

            get_sub_content(null);

            $country_obj.change(function() {
                get_sub_content($(this));
            });

            $region_obj.change(function() {
                get_sub_content($(this));
            });
            $self.data("initialized", true);
        });
    };

    /* ------------------------------------- */
    /* Default options */
    /* ------------------------------------- */
    $.fn.city_selector.defaults = {
    };

    $(document).ready(function() {
        $(".widget_city_holder").city_selector();
    });

})(jQuery);
