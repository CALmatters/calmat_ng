//  this handler is matched with the PopupSelect widget.  It's used to launch
//  the image change_list in __popup mode.  

(function($) {
        $(document).ready(function() {

            $('#choose_image').on('click', function (evt) {
                evt.preventDefault();

                popup_window = window.open(
                        "/admin/media_manager/mediaitem/?_popup=1000",
                        "_blank",
                        "toolbar=yes,scrollbars=yes,resizable=yes,top=500," +
                        "left=500,width=1250,height=800");
            });
        });
})(django.jQuery);