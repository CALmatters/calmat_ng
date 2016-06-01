/*
* idm_GA_FollowEventTracker
* This module will listen for a click on all elements within followElements().
* Each click event will manually call Google Analytics with a custom click event
* titled, 'Follow'.
*
* This method is much easier and less error-prone than manually adding an onClick
* attribute to each tag.
*
* Tracking a new element is as simple as appending a new element to the object
* returned by followElements().
*/
var idm_GA_FollowEventTracker = (function(){
    "use strict";
    
    function init(){
        addEventClickEventListenerToEach();
    };
    
    // These are the elements we will specifically target for this js module.
    function followElements(){
        return {
            article_follow_el: jQuery(".custom_follow_element"),
            subscribe_el: jQuery("#id-subscribe-form"),
            sidebar_subscribe_el: jQuery("#form_id_sidebar_subscribe")
        };
    };
    
    function addEventClickEventListenerToEach(){
        var _followElements = followElements();
            
        for(var el in _followElements){
            _followElements[el].click(function(){
                trigger_GA_follow_event();
            });
        };
    };
    
    function trigger_GA_follow_event(){
        ga('send', 'event', 'Follow', 'click', 'Follow story clicked');
    };
    
    // API
    return {
        init: init,
        showFollowElements: followElements
    };
    
})();