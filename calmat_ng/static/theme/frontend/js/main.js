
function initDynamicHeightElements() {

    // Dynamically set height for sidebar items when Desktop
    var winWidth = $(window).width();
    if(winWidth > 990) {
        // move placeholder atoms from article into sidebar
        $('div[id^=atom_sidebar_container_]').each(function(){
            var atom_id = this.id.match(/\d+$/)[0];
            var moveable_element = $('#atom_display_container_' + atom_id + ' .atom_moveable_element');
            if(moveable_element.length) {
                moveable_element.detach().appendTo($(this));
            }
        });
        
        // Set dynamic heights
        var total_height = jQuery('.dynamic-height-container').height();
        // console.log(total_height);
        var dynamic_height_items = jQuery('.dynamic-height');
        // console.log(dynamic_height_items);
        var item_count = dynamic_height_items.size();
        var item_height = total_height / item_count;
        if (total_height/item_count > 250) { // Only make dynamic if each item has at least 250px of space.
            dynamic_height_items.each(function() {
               var height_item = jQuery(this);
               height_item.height(item_height);
               // console.log(height_item);
               // console.log(height_item.height());
            });
        };
    } else {
        // move sidebar into content for mobile
        $('div[id^=atom_display_container_]').each(function(){
            var atom_id = this.id.match(/\d+$/)[0];
            var moveable_element = $('#atom_sidebar_container_' + atom_id + ' .atom_moveable_element');
            if(moveable_element.length) {
                moveable_element.detach().appendTo($(this));
            }
        });
    }

};
function getScrollbarWidth() {
    var div=$('<div style="width:50px;height:50px;overflow:hidden;position:absolute;top:-200px;left:-200px;"><div style="height:100px;"></div></div>');$('body').append(div);var w1=$('div',div).innerWidth();div.css('overflow-y','auto');var w2=$('div',div).innerWidth();$(div).remove();return(w1-w2);
}
function mobileCheck() {
    var winWidth = $(window).width();
    if (winWidth < 1200 - getScrollbarWidth()) {
        if (!$("body").hasClass("mobile-v")) {
            $(".recent-stories.r-articles .col4 article").each(function(index) {
                if (index == 2) { index = 0};
                $(this).addClass("col4goes").appendTo($(".recent-stories.r-articles .col").eq(index))
            });
            $("body").addClass("mobile-v");
        };
    } else {
        if ($("body").hasClass("mobile-v")) {
            $(".recent-stories.r-articles .col4goes").addClass("col4goes").appendTo($(".recent-stories.r-articles .col4"))
            $("body").removeClass("mobile-v");
        };
    }
    if (winWidth < 990 - getScrollbarWidth()) {
        if (!$("body").hasClass("mobile-v2")) {
            $(".partners-ships").prependTo($(".right-c-s"))
            $("body").addClass("mobile-v2");
        };
    } else {
        if ($("body").hasClass("mobile-v2")) {
            $(".partners-ships").appendTo($(".right-c-s"))
            $("body").removeClass("mobile-v2");
        };
    }
    if (winWidth < 767 - getScrollbarWidth()) {
        if (!$("body").hasClass("mobile-v3")) {
            $("div.stories").after($(".right-c-s .orange").addClass("orange-moved"))
            $("body").addClass("mobile-v3");
        };
    } else {
        if ($("body").hasClass("mobile-v3")) {
            $(".orange-moved").appendTo($(".right-c-s"));
            $(".orange-moved").removeClass(".orange-moved")
            $("body").removeClass("mobile-v3");
        };
    }
}

$(document).ready(function() {

    mobileCheck();
    $(window).resize(function() {
        mobileCheck();
    });

    // Open sidebar navigation on Bootstrap navbar-toggle click
    $('button.navbar-toggle').unbind('click')
                 .on('click', function(){
                    jQuery('body').addClass('active-left');
                 });

    $('.more-stories article .image a').fancybox();

    // $("input[type=checkbox], input[type=radio]").crfi();
    // $("select").crfs();

    if ($(".sidebar").length && $('.column_post_wrap').length == 0) {
        $(".sidebar").pin({
            containerSelector: ".pin-holder",
            minWidth: 990,
            padding: {
                top: 170,
                bottom: 170
            }
        });
    };

    $('[placeholder]').each(function() {  
        var input = $(this);
                    
        $(input).focus(function(){
            if (input.val() == input.attr('placeholder')) {
               input.val('').removeClass("placeholder");
            }
        });
            
        $(input).focus(function(){
            $(this).parent().addClass("active");
        });
            
        $(input).blur(function(){
           if (input.val() == '' || input.val() == input.attr('placeholder')) {
               input.val(input.attr('placeholder')).addClass("placeholder");
           }
        });
    }).blur();
    $(".team .btn-success").click(function() {

        window.setTimeout(function() {
            if ($(".team .error").length) {
                $('html, body').stop().animate({
                    scrollTop:  $(".team form").offset().top - $("#header").outerHeight()
                }, 0);
            };
        }, 100);
    });
    // rgc: not sure why this was here...caused issues: $("form").validate();

    // setup style to control article position indicator in crolled nav
    $('head').append('<style data-class="crolled-nav-after"></style>');

    var offset = $("#body").offset();
        $(window).scroll(function() {
            if ($(window).scrollTop() > offset.top ) {
                $("body").addClass("moved")

                // set article indicator on scoll
                var article_position_indicator_width = 100 * ($(window).scrollTop() - offset.top) / ($(document).height() - $(window).height() - offset.top);
                if(article_position_indicator_width < 0) article_position_indicator_width = 0;
                else if(article_position_indicator_width > 100) article_position_indicator_width = 100;
                $('head style[data-class="crolled-nav-after"]').replaceWith('<style data-class="crolled-nav-after">.crolled-nav:after{width:'
                     + article_position_indicator_width 
                     + '%}</style>');       
                // -- end article indicator


            } else {
                $("body").removeClass("moved")
        };
    });
    $('.accordion-content .accordion-item>h3').click(function(){
        var itemA = $('.accordion-content .accordion-item>h3');
        if( $(this).next().is(':hidden') ) {
            $(this).toggleClass('active').next().slideDown();
        } else {
            $(this).toggleClass('active').next().slideUp();
        }
        return false;
    }); 
        
    $(".crolled-nav .trigger").click(function() {
        $("body").toggleClass("active-left")
    });

    
    $(".orange h3").click(function() {
        $(this).parent().toggleClass("active");
        return false;
    });

    $(".main-wrapper").click(function() {
        if ($(this).hasClass("active-left")) {
            $("body").removeClass("active-left")
        };
    });


    /* Atom magnific popup
    --------------------------------------------------------------------------*/
    jQuery('.magnific').magnificPopup({
        // items: {
        //     src: '#atompopup',
        //     type: 'inline'
        // }
    });

    /* Post Sharing
    --------------------------------------------------------------------------*/
    jQuery('.post-meta .btns a.pr').on('click', function(e){
        e.preventDefault();
        window.print();
    });
});

$(window).load(function() {

    $('.headlines .slides').bxSlider({
        adaptiveHeight: true,
        controls: false,
        minSlides: 1,
        maxSlides: 3,
        infiniteLoop: false,
        slideWidth: 1000,
        slideMargin: 0
    });
    $('.grey-car .slides').bxSlider({
        pager: false,
        minSlides: 1,
        maxSlides: 4,
        infiniteLoop: false,
        hideControlOnEnd: true,
        slideWidth: 240,
        slideMargin: 30
    });
    var grey = $('.op_ed_question .slides').bxSlider({
        adaptiveHeight: true,
        pager: false,
        controls: ($('.op_ed_question .slides .slide .item').length > 2) ? true : false,
    });

    // Dynamic heights on load.
    initDynamicHeightElements();
    
    $(window).resize(function() {

        if (!(typeof grey.reloadSlider === 'undefined')) {
            window.setTimeout(function() {
                 grey.reloadSlider();
            }, 100);
        };
        // Dynamic heights on window resize as well.
        initDynamicHeightElements();

    });
    
    readMore.init(); // Initializes readMore module.

});

var readMore = (function(){
    "use strict";
    
    var settings = {
        shortcodes: ['[read more]','[ read more ]'] //-? Shortcodes this module will search for.
    };
    
    var selectors = {
        $readmore: findShortcode()
    };
    
    // Initialized this module.
    function init(){
        
        // Runs if we are on an atom's dedicated entry page and the shortcode exists in the atom's body.
        if(onAtomEntryPage() && shortcodeExists()){
            hideShortcode();
        // Runs if we are on an article page and the shortcode exists in the atom's body.
        }else if(onArticlePage() && shortcodeExists()){
            hideNextAll();
            hideShortcode();
        }
        else{};
    };

    // Determines by URL if we are on an atom dedicated entry page or not.
    function onAtomEntryPage(){
        if(window.location.href.indexOf('/atom/') == -1){
            return false;
        }else{
            return true;
        };
    };
    
    // Determines by URL if we are on an article page.
    function onArticlePage(){
        if(window.location.href.indexOf('/articles/') == -1){
            return false;
        }else{
            return true;
        }
    }
    
    // Finds and returns jQuery object of shortcode found within atom body.
    function findShortcode(){
        var self = this,
            shortcodes = settings.shortcodes,
            $shortcode = null;
        
        for(var i in shortcodes){
            var _shortcode = shortcodes[i],
                parent = onAtomEntryPage() ? '.entry':'.atom_block'; // parent element depends upon if we are on atom entry page.
            
            if (jQuery(parent + " p:contains('" + _shortcode + "')").length > 0){
                console.log(_shortcode + ' shortcode found.');
                $shortcode = jQuery(parent + " p:contains('" + _shortcode + "')");
            };
        };
        
        return $shortcode; 
    };
    
    // Returns boolean determining if shortcode exists in current loaded page or not.
    function shortcodeExists(){
        var exists = (selectors.$readmore != null) ? true:false;
        
        return exists
    };
    
    // Hides all elements below the shortcode.
    function hideNextAll(){
        var $readmore = selectors.$readmore;
            
        $readmore.nextAll().hide(0);
    };
    
    // Hides the shortcode itself from the atom body.
    function hideShortcode(){
        var $readmore = selectors.$readmore;
        
        $readmore.hide(0);
    };
    
    // readMore API
    return {
        init: init, // API: Initializes the module.
        findShortcode: findShortcode, // API: Finds and returns jQuery object of shortcode found within atom body.
        shortcodeExists: shortcodeExists // API: Returns boolean determining if shortcode exists in current loaded page or not.
    };
    
})();