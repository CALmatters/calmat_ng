
function get_cat_url_arg() {
    var cat_id_str = jQuery("#categories").text().trim();
    console.log(cat_id_str);
    if(cat_id_str)
        return "cats="+cat_id_str;
}

function subscribe_submit(form_element) {
    // Sends any form, but used for the subscription form
    // form.action must point to a POST processing URL
    // the form processing URL must lead to a view that can handle the form

    var senddata = jQuery(form_element).serialize();
    var cats_url_arg = get_cat_url_arg();
    if(cats_url_arg)
        senddata += '&' + cats_url_arg;

    jQuery.ajax({
        type: 'POST',
        url: jQuery(form_element).attr('action'),
        data: senddata,
        success: function (data) {
            jQuery(form_element).replaceWith('<p style="padding-bottom:20px"><b>Thank you!</b></p>');
        }
    });

    event.preventDefault();
    return false;
}

function subscribe_submit_no_form(email_addr, success_func) {

    var senddata = "email="+email_addr;
    var cats_url_arg = get_cat_url_arg();
    if(cats_url_arg)
        senddata += '&' + cats_url_arg;

    jQuery.ajax({
        type: 'POST',
        url: '/subscribe/',
        data: senddata,
        success: function (data) {
            success_func();
        }
    });


}