var file_glue = (function(){
    "use strict";
    
    var run = {
        
        init: function(){
            minimalize_controls_for_popup();
            remove_all_a_href();

        },
        
        selectClicked: function($this){
            var imgUrl = getSelectedImgUrl($this);
            var thumb = getSelectedImgThumb($this);

            insertImgUrlIntoInput(imgUrl, thumb);
            closeMedia_ManagerWindow();
        }
    }

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
    };
    
    // Returns the url for the selected image.
    function getSelectedImgUrl($this){
        var imgUrl = $this.data("media-upload-url");
        
        return imgUrl;
    };

    function getSelectedImgThumb($this){
        var thumb = django.jQuery($this.parents('tr').find('.field-admin_thumb img')).attr('src');

        console.log("Thumb:  "+thumb);

        return thumb
    }

    // Inserts the image url into the 'Image URL' input field in the 'Insert/Edit Image' popup window.
    function insertImgUrlIntoInput(imgUrl, thumb){
        
        function getInsertEditIframeID(){
            return '#' + parent.window.document.querySelectorAll("iframe[id^='mce_']")[0].getAttribute("id");
        };

        if(!opener) {
            var insertEditIframeID = getInsertEditIframeID(),
                image_url_input =
                    parent // escapes out of the iFrame into the parent window.
                        .window.document.querySelector(insertEditIframeID).contentDocument // selects Document object of the 'Insert/Edit Image' iFrame.
                        .querySelector("#src"); // targets the 'Image URL' input field.

            image_url_input.value = imgUrl;
        } else {

            //  This section is largely copied from FB_FileBrowseField.FileSubmit
            //  FileBrowser.show() is opening the window, but this code is
            //  handling the submit.
            // var input_id = window.name;
            var input_id_selector = "#id_image";
            // var help_id_selector = '#help_' + input_id;
            var preview_link_selector = '#preview_image';
            var preview_img_selector = '#preview_image img';
            var clear_id_selector = '#clear_image';

            opener.document.querySelector(preview_img_selector).src = thumb;
            opener.document.querySelector(preview_link_selector).href = imgUrl;
            opener.document.querySelectorAll(input_id_selector)[0].value = imgUrl;

            django.jQuery(opener.document.querySelector(preview_link_selector)).show();
            django.jQuery(opener.document.querySelector(clear_id_selector)).show();
            django.jQuery(opener.document.querySelector(preview_img_selector)).show();
        }
    };
    
    // Closes the media_manager popup window.
    function closeMedia_ManagerWindow(){

        if(!opener) {
            //  When the opener is a TinyMCE image diaglog, and we are the filebrowser.
            var all_mce_CloseButtons = parent.window.document.querySelectorAll(".mceClose"),
                latest_mce_CloseButton = all_mce_CloseButtons[all_mce_CloseButtons.length - 1];

            latest_mce_CloseButton.click();
        } else {
            //  When the opener is anything else - is this OK?
            window.close();
        }
    };
    
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