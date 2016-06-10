/*
requires: var custom_follow_csrf_token to get set
*/

    function custom_follow_clicked(type, type_id){
        // detect if subscriber exists
        match = document.cookie.match(new RegExp('is_subscriber' + '=([^;]+)'));
        if (match != null) {
            custom_follow_show_form(type, type_id, match[1]);
        } else {
            custom_follow_show_form(type, type_id);
        }
    }
    function custom_follow_show_form(type, type_id, subscriber_id){
        var new_element = ''
            + '<form class="custom_follow_element" method="post" action="/follow/?type=' + type +'&id=' + type_id + '&ref=internal"'
            + '  class="rss" style="float:left;padding:0 6px;height:31px;background:url(/static/theme/frontend/img/bg_follow.png);box-shadow:0 0 3px rgba(0, 0, 0, .5);" '
            + '  onsubmit="custom_follow_form_submit(this, \'' + type + '\', ' + type_id + ');event.preventDefault();return false;">'
            + custom_follow_csrf_token;
        if(subscriber_id > 0) {
            new_element = new_element + ' <input name="subscriber_id" type="hidden" value="' + subscriber_id + '" ';
        } else {
            new_element = new_element + ' <input name="email" type="email" maxlength="75" placeholder="Email Address" '
        }
        new_element = new_element + ''
            + '  style="font-weight: 500;padding:0px 4px;height: 25px;border:none;vertical-align: middle;border-radius: 3px; font-size:16px;" />'
            + '</form>';
        jQuery('.custom_follow_element').replaceWith(new_element);
        if(subscriber_id > 0) jQuery('.custom_follow_element:first').submit(); // only submit one button click
    }
    function custom_follow_form_submit(formobj, type, type_id, subscriber_id){
        jQuery.ajax({
            type: 'POST',
            url: jQuery(formobj).attr('action'),
            data: jQuery(formobj).serialize(),
            success: function (data) {
                custom_follow_show_following(type, type_id);
                jQuery('.custom_follow_element').popover('show');
            }
        });
    }
    function custom_follow_unfollow(type, type_id){
        jQuery.ajax({
            type: 'GET',
            url: '/unfollow/?type=' + type +'&id=' + type_id,
            success: function (data) {
                custom_follow_show_follow(type, type_id);
            }
        });
    }
    function custom_follow_show_following(type, type_id){
        jQuery('.custom_follow_element').replaceWith(''
            + '<a href="javascript:void(0);" onclick="custom_follow_unfollow(\'' + type + '\', ' + type_id + ');"'
            + '  class="custom_follow_element"' 
            + ' data-toggle="popover" data-trigger="manual" data-placement="top"'
            + ' data-content="Thank you. We will keep you updated as this story evolves."'
            + '  onmouseover="jQuery(\'.custom_follow_mouseover_text\').html(\'UNFOLLOW\');" onmouseout="jQuery(\'.custom_follow_mouseover_text\').html(\'FOLLOWING\');jQuery(this).popover(\'hide\');">'
            + '<i class="fa fa-rss"></i><span class="custom_follow_mouseover_text">FOLLOWING</span></a>'
        );
    }
    function custom_follow_show_follow(type, type_id){
        // send to normal follow on mobile
        if($(window).width() < 1050) {
            new_element = '<a href="/follow/?type=' + type + '&id=' + type_id + '&ref=internal" target="_blank" '
                + ' class="custom_follow_element"><i class="fa fa-rss"></i><span>FOLLOW</span></a>';
        } 
        else {
            new_element = '<a href="javascript:void(0);" '
                + ' onclick="jQuery(this).popover(\'hide\');custom_follow_clicked(\'' + type + '\', ' + type_id + ');"'
                + ' onmouseover="jQuery(this).popover(\'show\');"'
                + ' onmouseout="jQuery(this).popover(\'hide\');"'
                + ' data-toggle="popover" data-trigger="manual" data-placement="top"'
                + ' data-content="You can get updates as this story develops in the political process."'
                + ' class="custom_follow_element"><i class="fa fa-rss"></i><span>FOLLOW THIS STORY</span></a>';
        }

        jQuery('.custom_follow_element').replaceWith(new_element);
    }

    function newsletter_ajax_submit(form_element) {
        // add token
        jQuery(custom_follow_csrf_token).appendTo(form_element);
        
        // submit this
        jQuery.ajax({
            type: 'POST',
            url: jQuery(form_element).attr('action'),
            data: jQuery(form_element).serialize(),
            success: function (data) {
                jQuery(form_element).replaceWith('<p style="padding-bottom:20px"><b>Thank you!</b></p>');
            }
        });

        event.preventDefault();        
        return false;
    }