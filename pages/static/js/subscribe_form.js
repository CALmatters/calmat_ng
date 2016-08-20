

$(document).ready(function() {

    $("a#follow_btn").on('click', function(evt){
        console.log("Submit email started");
        evt.preventDefault();

        var $this = $(this);

        $("a#follow_btn").off('click');

        $this.html('<i class="fa fa-rss"></i><input type="text" id="email_textbox" class="follow_email_textbox" name="email" placeholder="email" value=""/>');

        $("#email_textbox").off('click').on('keypress', function(evt){

            var code = evt.keyCode || evt.which;
            console.log(code);
            if(code == 13) { //Enter keycode
                subscribe_submit_no_form($('#email_textbox').val(), function($) {
                    $this.html('<i class="fa fa-rss"></i> Thank You');
                });
                
             }
        });
    });
});