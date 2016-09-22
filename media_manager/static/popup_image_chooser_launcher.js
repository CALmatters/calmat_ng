//  this handler is matched with the PopupSelect widget.  It's used to launch
//  the image change_list in __popup mode.  

(function($) {
        $(document).ready(function() {

            $('.choose_image').on('click', function (evt) {
                evt.preventDefault();

                //  Set current target field to insert result when item is
                //  chosen in the popup.   The pop will look for this element
                //  to determine where to install result.
                //  TODO:  This is a brittle, time sensitive solution. fix it.

                var target_field_name = $(this).parent().find('select').attr('name');
                var body = $('body');
                var span = body.find('#target_field')[0];
                if(span == undefined)
                    span = $('<span id="target_field" style="display: block">');
                else
                    span = $(span);
                span.html(target_field_name);
                body.append(span);

                popup_window = window.open(
                        "/admin/media_manager/mediaitem/?_popup=1000",
                        "_blank",
                        "toolbar=yes,scrollbars=yes,resizable=yes,top=500," +
                        "left=500,width=1250,height=800");
            });
        });
})(django.jQuery);