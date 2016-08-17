
function subscribe_submit(form_element) {
    // Sends any form, but used for the subscription form
    // form.action must point to a POST processing URL
    // the form processing URL must lead to a view that can handle the form

    var senddata = jQuery(form_element).serialize();
    var cats = "cats="+jQuery("#categories").text().trim();  //  Should be a list of cat ids
    if(cats)
        senddata += '&' + cats;

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