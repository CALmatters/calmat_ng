var file_glue = (function(){
    "use strict";
    
    var run = {
        
        init: function(){
            minimalize_controls_for_popup();
            remove_all_a_href();

        },
        
        selectClicked: function($this){
            var imgID = getSelectedImgID($this);
            var imgUrl = getSelectedImgUrl($this);
            var thumb = getSelectedImgThumb($this);

            insertImgUrlIntoInput(imgID, imgUrl, thumb);
            closeMedia_ManagerWindow();
        }
    };

    //  Removes left menu, headers, and add button, so it's just a image
    //  selection dialog.  Needed for popup version, but should not be used,
    //  nor any javascript from here, in the admin version.
    function minimalize_controls_for_popup() {
        django.jQuery("#header").remove();
        django.jQuery("#side-panel").remove();
        django.jQuery(".object-tools").remove();
        django.jQuery(".action-checkbox").remove();
    }

    // Removes all a href's that wrap the result-list buttons. This is a hacky way of resolving the problem.
    // Would be ideal to look into a way of removing these a href's server-side.
    function remove_all_a_href(){
        var buttons = document.querySelectorAll(".results a[href*='media_manager'] button");
        
        // loops through all buttons and replace's it's parentNode with the button element itself.
        for (var i=0; i < buttons.length; i++){
            var _button = buttons[i],
                _button_parentNode = _button.parentNode;
            
            _button_parentNode.outerHTML = _button.outerHTML;
        }
    }


    function getSelectedImgID($this){
        return $this.data("media-upload-id");
    }

    function getSelectedImgUrl($this){
        return $this.data("media-upload-url");
    }

    function getSelectedImgThumb($this){
        var thumb = django.jQuery($this.parents('tr').find('.field-admin_thumb img')).attr('src');

        console.log("Thumb:  "+thumb);

        return thumb
    }

    // Inserts the image url into the 'Image URL' input field in the 'Insert/Edit Image' popup window.
    function insertImgUrlIntoInput(imgID, imgUrl, thumb){


        if(!opener) {
            //  When launch from inside TinyMCE
            top.tinymce.activeEditor.windowManager.getParams().oninsert(imgUrl);
        } else {
            //  When launched from popup_launcher for fields of PopupSelect
            var input_id_selector = "#id_image";
            var preview_link_selector = '#preview_image';
            var preview_img_selector = '#preview_image img';
            var clear_id_selector = '#clear_image';

            opener.document.querySelector(preview_img_selector).src = thumb;
            opener.document.querySelector(preview_link_selector).href = imgUrl;
            opener.document.querySelectorAll(input_id_selector)[0].value = imgID;

            django.jQuery(opener.document.querySelector(preview_link_selector)).show();
            django.jQuery(opener.document.querySelector(clear_id_selector)).show();
            django.jQuery(opener.document.querySelector(preview_img_selector)).show();

            //  When user chooses a person in the media item dialog for the featured image
            //  this code will find the media item, and insert the description and credit
            //  as defaults.   Note that this ajax call is synchronous, because if the window
            //  dialog closes before the function returns it doesn't set the values.   So,
            //  this code will block, waiting for a response, and then allow the window to be closed.
            //  Todo:   DRY it out - There is code in copy_forward_image_data.js that does the same thing
            
            django.jQuery.ajax({
                url:'/media_lookup/'+imgID+'/',
                async: false,
                success: function( data ) {
                    opener.document.querySelector("#id_featured_image_description").value = data.desc;
                    opener.document.querySelector("#id_featured_image_credit").value = data.credit;
                }});
        }
    }
    
    // Closes the media_manager popup window.
    function closeMedia_ManagerWindow(){

        if(!opener) {
            //  When launch from inside TinyMCE
            top.tinymce.activeEditor.windowManager.close();
        } else {
            //  When the opener is anything else - is this OK?
            window.close();
        }
    }
    
    // API
    return {
        init: run.init,
        selectClicked: run.selectClicked       
    }
    
})();


django.jQuery(document).ready(function(){
    
    file_glue.init();
    
    django.jQuery(".results button").click(function(evt){
        evt.preventDefault();

        var $this = django.jQuery(this);

        console.log('Button Clicked');

        file_glue.selectClicked($this);
    });
    
});