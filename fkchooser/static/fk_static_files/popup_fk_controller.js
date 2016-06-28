var file_glue = (function(){
    "use strict";
    
    var run = {
        
        init: function(){
            minimalize_controls_for_popup();
            remove_all_a_href();

        },
        
        selectClicked: function($this){
            var fkID = getFKID($this);
            window.opener.save(fkID);
            window.close();
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


    function getFKID($this){
        return $this.data("fk-id");
    }

    // Inserts the image url into the 'Image URL' input field in the 'Insert/Edit Image' popup window.
    // function insertImgUrlIntoInput(imgID, fieldID){
    //     var id_field = "#"+fieldID;
    //     opener.document.querySelectorAll(id_field)[0].value = imgID;
    // }
    
    // Closes the media_manager popup window.
    function closeMedia_ManagerWindow(){
        window.close();
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