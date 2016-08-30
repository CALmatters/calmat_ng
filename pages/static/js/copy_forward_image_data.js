// http://localhost:8000/media_lookup/6/



//  When user chooses a person in the Article Featured Image menu
//  this code will find the media item, and insert the description and credit
//  as defaults.
//  Todo:   DRY it out - There is code in popup_v1.js that does the same thing
(function($) {
    $(document).ready(function () {
        $('select#id_image').change(function (evt) {
            var media_id = $("select#id_image option:selected").val();
            $.get('/media_lookup/'+media_id+'/', function( data ){
                document.querySelector("#id_featured_image_description").value = data.desc;
                document.querySelector("#id_featured_image_credit").value = data.credit;
            });
        });
    });
})(django.jQuery);