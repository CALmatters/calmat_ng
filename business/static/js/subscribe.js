
function subscribe_submit(form_element) {
    // Sends any form, but used for the subscription form
    // form.action must point to a POST processing URL
    // the form processing URL must lead to a view that can handle the form

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